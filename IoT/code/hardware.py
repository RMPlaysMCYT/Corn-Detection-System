# hardware.py
import time
import cv2
from gpiozero import AngularServo

class Camera:
    """Wrapper for the camera (OpenCV)."""
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
    
    def read_frame(self):
        """Return a single frame (numpy array) or None if failed."""
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        self.cap.release()

class Servo:
    """Wrapper for the SG90 servo."""
    def __init__(self, pin=18, min_pulse=0.0006, max_pulse=0.0023,
                 default_angle=0, reject_angle=90):
        self.servo = AngularServo(pin,
                                  min_pulse_width=min_pulse,
                                  max_pulse_width=max_pulse)
        self.default_angle = default_angle
        self.reject_angle = reject_angle
        self.servo.angle = default_angle  # home position
    
    def reject(self):
        """Move to reject angle, then back to default."""
        self.servo.angle = self.reject_angle
        time.sleep(0.5)   # allow seed to fall
        self.servo.angle = self.default_angle
        time.sleep(0.5)   # settle
    
    def detach(self):
        self.servo.detach()