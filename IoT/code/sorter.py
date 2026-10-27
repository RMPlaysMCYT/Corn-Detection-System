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
    
    def start(self):
        """Start sorting in a background thread."""
        if self.running:
            return
        self.running = True
        self.total_processed = 0
        self.healthy_count = 0
        self.unhealthy_count = 0
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

            seed_present, _ = self.has_seed(frame)

            # Only classify+count when there IS a seed AND we're not in cooldown
            if seed_present and not self._in_cooldown():
                is_healthy, confidence = self.classifier.is_healthy(frame, threshold=0.8)
                self.total_processed += 1
                ...
                self._start_cooldown(1.5)  # seconds, so the same seed isn't counted again

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

    def has_seed(self, frame, prev_gray=None):
        """
        Returns (seed_present, new_prev_gray).
        A crude 'is something bright/dark in the ROI' check.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Look at the centre region only — where seeds pass
        h, w = gray.shape
        roi = gray[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
        # Blur + threshold: seeds are darker than the conveyor belt
        blur = cv2.GaussianBlur(roi, (7, 7), 0)
        _, thresh = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Count contours with a plausible seed area
        seed_contours = [c for c in contours if 200 < cv2.contourArea(c) < 20000]
        return (len(seed_contours) > 0), gray

    def _in_cooldown(self):
        return time.time() - getattr(self, '_last_trigger', 0) < getattr(self, '_cooldown', 1.5)

    def _start_cooldown(self, seconds):
        self._last_trigger = time.time()
        self._cooldown = seconds