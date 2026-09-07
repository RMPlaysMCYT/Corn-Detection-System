# sorter.py
import threading
import time

class Sorter:
    """
    Manages the sorting process in a background thread.
    Communicates with the GUI via callbacks.
    """
    def __init__(self, camera, servo, classifier, hopper_empty_callback, update_callback):
        self.camera = camera
        self.servo = servo
        self.classifier = classifier
        self.hopper_empty_callback = hopper_empty_callback   # called when done
        self.update_callback = update_callback               # called after each seed
        
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
            
            # 2. Run inference
            is_healthy, confidence = self.classifier.is_healthy(frame, threshold=0.8)
            
            # 3. Update counters
            self.total_processed += 1
            if is_healthy:
                self.healthy_count += 1
            else:
                self.unhealthy_count += 1
                # 4. Reject unhealthy seed (only if confident)
                self.servo.reject()
            
            # 5. Notify GUI about progress (thread‑safe via callback)
            if self.update_callback:
                self.update_callback(self.total_processed,
                                     self.healthy_count,
                                     self.unhealthy_count)
            
            # 6. CHECK FOR EMPTY HOPPER
            #    Replace this with your actual sensor logic.
            #    For demo, we simulate a hopper that runs out after a few seeds.
            #    In real use, you might check a GPIO pin, or detect no more seeds in frame.
            if self._is_hopper_empty():
                self.running = False
                break
            
            # Short delay to prevent thrashing
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