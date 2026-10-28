import threading
import time
import cv2
import numpy as np

class Sorter:
    """
    Manages the sorting process in a background thread.
    Communicates with the GUI via callbacks.
    """
    def __init__(self, camera, servo, classifier, hopper_empty_callback, update_callback):
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
        self._seed_latched = False
        self._empty_frames = 0
    
    def start(self):
        """Start sorting in a background thread."""
        if self.running:
            return
        self.running = True
        self.total_processed = 0
        self.healthy_count = 0
        self.unhealthy_count = 0
        self._seed_latched = False
        self._empty_frames = 0
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Gracefully stop the sorting loop."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
    
    def _run(self):
        """Main sorting loop – runs in the background thread."""
        while self.running:
            # 1. Read a frame from the camera
            frame = self.camera.read_frame()
            if frame is None:
                time.sleep(0.05)
                continue

            seed_present = self.has_seed(frame)

            if seed_present:
                self._empty_frames = 0
                if not self._seed_latched:
                    is_healthy, confidence = self.classifier.is_healthy(frame, threshold=0.8)
                    self.total_processed += 1
                    if is_healthy:
                        self.healthy_count += 1
                    else:
                        self.unhealthy_count += 1
                        self.servo.reject()
                    print(f"[Sorter] seed #{self.total_processed}: "
                        f"{'HEALTHY' if is_healthy else 'UNHEALTHY'} conf={confidence:.2f}")
                    self._seed_latched = True
            else:
                self._empty_frames += 1
                if self._empty_frames >= 3:
                    self._seed_latched = False

            # Always update the GUI so the user sees it's alive
            if self.update_callback:
                self.update_callback(self.total_processed,
                                    self.healthy_count,
                                    self.unhealthy_count)

            time.sleep(0.1)
        
        # When loop ends, call the "complete" callback
        if self.hopper_empty_callback:
            self.hopper_empty_callback(self.total_processed,
                                       self.healthy_count,
                                       self.unhealthy_count)
    
    def _is_hopper_empty(self):
        """
        Replace with real sensor logic.
        For simulation, we stop after 30-80 random seeds.
        You could also detect that the camera frame has no seeds (e.g., using contour detection).
        """
        # This is a dummy – you can replace with e.g.:
        #   return not gpio.input(HOPPER_SENSOR_PIN)
        # For now, we stop after we've processed a certain number (simulated).
        # We'll make it stop after about 50 seeds on average.
        if not hasattr(self, '_max_seeds'):
            import random
            self._max_seeds = random.randint(30, 80)
        return self.total_processed >= self._max_seeds

    def has_seed(self, frame):
        h, w = frame.shape[:2]

        # Use most of the view so seeds need not pass through the exact center.
        y0, y1 = int(h * 0.1), int(h * 0.9)
        x0, x1 = int(w * 0.1), int(w * 0.9)
        roi = frame[y0:y1, x0:x1]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        brightness = cv2.GaussianBlur(hsv[:, :, 2], (7, 7), 0)

        # Corn is often more saturated than a white background; also detect
        # kernels that are simply darker than the local background.
        background_brightness = float(np.median(brightness))
        value_threshold = max(0, int(background_brightness) - 25)
        _, value_mask = cv2.threshold(
            brightness, value_threshold, 255, cv2.THRESH_BINARY_INV
        )
        saturation_mask = cv2.inRange(saturation, 35, 255)
        mask = cv2.bitwise_or(value_mask, saturation_mask)
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8)
        )

        # Save debug images every ~20 frames (so we can look at the picture)
        self._debug_frame_count = getattr(self, '_debug_frame_count', 0) + 1
        if self._debug_frame_count % 20 == 0:
            cv2.imwrite("/tmp/sorter_roi.png", brightness)
            cv2.imwrite("/tmp/sorter_mask.png", mask)
            print(f"[Sorter] ROI mean brightness = {background_brightness:.1f}")

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(c) for c in contours]
        big = [a for a in areas if 200 < a < 20000]
        return len(big) > 0
