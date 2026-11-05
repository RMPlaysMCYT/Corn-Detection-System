import threading
import time
import cv2
import numpy as np


class Sorter:
    """
    Manages the sorting process in a background thread.
    Communicates with the GUI via callbacks.
    """

    # Frames of "no seed" required before declaring the hopper empty.
    # At ~10 Hz effective rate (and ~0.6 Hz during sort_seed blocking),
    # 50 frames ≈ 5–8 s of continuous emptiness.
    EMPTY_CONFIRMATION_FRAMES = 50

    # Ignore "empty" verdicts for the first N frames after startup so the
    # camera AE/AWB can settle and the first seed can enter the ROI.
    STARTUP_GRACE_FRAMES = 30

    # Frames of "seed present" required before counting/sorting, to reject
    # single-frame noise.
    SEED_CONFIRMATION_FRAMES = 2

    def __init__(self, camera, servo, classifier,
                 hopper_empty_callback, update_callback):
        self.camera = camera
        self.servo = servo
        self.classifier = classifier
        self.hopper_empty_callback = hopper_empty_callback
        self.update_callback = update_callback

        self.running = False
        self.thread = None

        # Counters
        self.total_processed = 0
        self.healthy_count = 0
        self.unhealthy_count = 0

        # Latch / confirmation state
        self._seed_latched = False
        self._seed_present_frames = 0
        self._empty_frames = 0
        self._frames_seen = 0
        self._conveyors_started = False

        # Debug
        self._debug_frame_count = 0

    # ------------------------------------------------------------------ #
    #  Lifecycle
    # ------------------------------------------------------------------ #
    def start(self):
        """Start sorting in a background thread."""
        if self.running:
            return
        self.running = True
        self.total_processed = 0
        self.healthy_count = 0
        self.unhealthy_count = 0
        self._seed_latched = False
        self._seed_present_frames = 0
        self._empty_frames = 0
        self._frames_seen = 0
        self._conveyors_started = False
        self._debug_frame_count = 0
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """Gracefully stop the sorting loop."""
        self.running = False
        if self.thread:
            # sort_seed() blocks ~1.7 s; give the thread time to finish.
            self.thread.join(timeout=2.5)
        try:
            self.servo.stop_conveyors()
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    #  Main loop
    # ------------------------------------------------------------------ #
    def _run(self):
        try:
            while self.running:
                frame = self.camera.read_frame()
                if frame is None:
                    time.sleep(0.05)
                    continue

                self._frames_seen += 1

                # Start the belt only after the first real frame arrives.
                if not self._conveyors_started:
                    print("[Sorter] First frame received — starting conveyors")
                    self.servo.start_conveyors()
                    self._conveyors_started = True

                seed_present = self.has_seed(frame)

                if seed_present:
                    self._empty_frames = 0
                    self._seed_present_frames += 1
                    if (not self._seed_latched
                            and self._seed_present_frames >= self.SEED_CONFIRMATION_FRAMES):
                        self._handle_seed(frame)
                else:
                    self._seed_present_frames = 0
                    self._empty_frames += 1
                    if self._empty_frames >= 3:
                        self._seed_latched = False

                    # Only allow the empty-stop after the startup grace window.
                    if (self._frames_seen > self.STARTUP_GRACE_FRAMES
                            and self._empty_frames >= self.EMPTY_CONFIRMATION_FRAMES):
                        print("[Sorter] Hopper appears empty; stopping conveyors")
                        self.servo.stop_conveyors()
                        self.running = False

                if self.update_callback:
                    self.update_callback(
                        self.total_processed,
                        self.healthy_count,
                        self.unhealthy_count,
                    )

                time.sleep(0.1)

        except Exception as e:
            print(f"[Sorter] Unhandled exception in loop: {e}")
        finally:
            # Always call the completion callback exactly once.
            if self.hopper_empty_callback:
                self.hopper_empty_callback(
                    self.total_processed,
                    self.healthy_count,
                    self.unhealthy_count,
                )

    def _handle_seed(self, frame):
        """Stopper → classify → flip sorter. Called from _run() only."""
        # 1. Capture the seed under the camera.
        self.servo.trigger_stopper()

        # 2. Classify the captured frame.
        is_healthy, confidence = self.classifier.is_healthy(
            frame, threshold=0.8
        )

        self.total_processed += 1
        if is_healthy:
            self.healthy_count += 1
            status = "healthy"
        else:
            self.unhealthy_count += 1
            status = "unhealthy"

        # 3. Flip the sorter arm to the right bin.
        self.servo.sort_seed(status)
        print(f"[Sorter] seed #{self.total_processed}: "
              f"{status.upper()} conf={confidence:.2f}")

        self._seed_latched = True
        self._seed_present_frames = 0

    # ------------------------------------------------------------------ #
    #  Seed detection
    # ------------------------------------------------------------------ #
    def has_seed(self, frame):
        h, w = frame.shape[:2]

        # Wider ROI so seeds need not pass through the exact centre.
        y0, y1 = int(h * 0.10), int(h * 0.90)
        x0, x1 = int(w * 0.10), int(w * 0.90)
        roi = frame[y0:y1, x0:x1]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        brightness = cv2.GaussianBlur(hsv[:, :, 2], (7, 7), 0)

        background_brightness = float(np.median(brightness))

        # Floor the threshold so a dark belt doesn't produce an all-white mask,
        # and so a bright belt doesn't hide dark kernels.
        value_threshold = max(40, int(background_brightness) - 25)
        _, value_mask = cv2.threshold(
            brightness, value_threshold, 255, cv2.THRESH_BINARY_INV
        )
        saturation_mask = cv2.inRange(saturation, 60, 255)

        mask = cv2.bitwise_or(value_mask, saturation_mask)
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8)
        )

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        areas = [cv2.contourArea(c) for c in contours]
        big = [a for a in areas if 200 < a < 20000]

        # Debug: dump every 20th frame plus the first 5 (so you can see startup).
        self._debug_frame_count += 1
        if self._debug_frame_count <= 5 or self._debug_frame_count % 20 == 0:
            try:
                cv2.imwrite("/tmp/sorter_roi.png", brightness)
                cv2.imwrite("/tmp/sorter_mask.png", mask)
                cv2.imwrite("/tmp/sorter_full.png", frame)
                print(f"[Sorter] dbg#{self._debug_frame_count} "
                      f"bg={background_brightness:.1f} "
                      f"vt={value_threshold} "
                      f"contours={len(big)} "
                      f"seed={len(big) > 0}")
            except Exception as e:
                print(f"[Sorter] debug write failed: {e}")

        return len(big) > 0