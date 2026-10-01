import time
import cv2
import platform

def is_raspberry_pi():
    try:
        with open("/proc/device-tree/model", "r", encoding="utf-8") as f:
            model = f.read()
        return "Raspberry" in model
    except Exception:
        return False

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


if platform.system() == "Linux" and is_raspberry_pi():
    try:
        # For Raspberry Pi 5, we import standard AngularServo.
        # Ensure python3-lgpio is installed so it uses the correct backend automatically.
        from gpiozero import AngularServo
    except Exception:
        print("[WARN] Pi GPIO not available; using mock servo.")
        class Servo:
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
    else:
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
        """Mock servo for testing off-Pi (e.g. Windows or a Linux PC) — logs instead of moving hardware."""
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