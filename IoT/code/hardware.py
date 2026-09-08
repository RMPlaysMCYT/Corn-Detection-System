# hardware.py
import time
import cv2
import platform

class Camera:
    """Wrapper for the camera (OpenCV)."""
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

    def read_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()


if platform.system() == "Linux":
    from gpiozero import AngularServo, Device
    from gpiozero.pins.pigpio import PiGPIOFactory
    Device.pin_factory = PiGPIOFactory()

    class Servo:
        """Wrapper for the SG90 servo (real hardware, Raspberry Pi only)."""
        def __init__(self, pin=18, min_pulse=0.0006, max_pulse=0.0023,
                     default_angle=0, reject_angle=90):
            self.servo = AngularServo(pin, min_pulse_width=min_pulse, max_pulse_width=max_pulse)
            self.default_angle = default_angle
            self.reject_angle = reject_angle
            self.servo.angle = default_angle

        def reject(self):
            self.servo.angle = self.reject_angle
            time.sleep(0.5)
            self.servo.angle = self.default_angle
            time.sleep(0.5)

        def detach(self):
            self.servo.detach()

else:
    class Servo:
        """Mock servo for testing off-Pi (e.g. Windows) — logs instead of moving hardware."""
        def __init__(self, pin=18, min_pulse=0.0006, max_pulse=0.0023,
                     default_angle=0, reject_angle=90):
            self.default_angle = default_angle
            self.reject_angle = reject_angle
            print(f"[MockServo] Initialized on virtual pin {pin}")

        def reject(self):
            print("[MockServo] Rejecting seed...")
            time.sleep(0.3)

        def detach(self):
            print("[MockServo] Detached")