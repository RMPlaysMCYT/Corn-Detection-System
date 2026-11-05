import time
import cv2
import platform
import numpy as np

from picamera2 import Picamera2

def is_raspberry_pi():
    try:
        with open("/proc/device-tree/model", "r", encoding="utf-8") as f:
            model = f.read()
        return "Raspberry" in model
    except Exception:
        return False

class Camera:
    """
    Camera wrapper using picamera2, required for Raspberry Pi 5 / Bookworm.
    Returns frames in BGR format, compatible with the rest of your pipeline.
    """
    def __init__(self, camera_id=0):
        self.picam = Picamera2()
        
        config = self.picam.create_preview_configuration(
            main={"size": (1080, 1080), "format": "RGB888"}
        )
        self.picam.configure(config)
        self.picam.start()
        
        time.sleep(1.5)

    def read_frame(self):
        try:
            # capture_array returns an RGB888 numpy array
            frame_rgb = self.picam.capture_array()
            
            # Convert RGB to BGR for OpenCV compatibility
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            return frame_bgr
        except Exception as e:
            print(f"[Camera] capture_array() error: {e}")
            return None

    def release(self):
        try:
            self.picam.stop()
        except Exception:
            pass

CONVEYOR_1_PIN = 18  # Physical pin 12, BCM GPIO 18
CONVEYOR_2_PIN = 12  # Physical pin 32, BCM GPIO 12
STOPPER_PIN = 13  # Physical pin 33, BCM GPIO 13
SORTER_PIN = 19  # Physical pin 35, BCM GPIO 19
MIN_PULSE_WIDTH = 0.0005
MAX_PULSE_WIDTH = 0.0025


if platform.system() == "Linux" and is_raspberry_pi():
    try:
        from gpiozero import AngularServo, Servo as ContinuousServo
    except Exception:
        print("[WARN] Pi GPIO not available; using mock servos.")
        _USE_REAL_SERVOS = False
    else:
        _USE_REAL_SERVOS = True
else:
    _USE_REAL_SERVOS = False


class ServoController:
    """Controls two continuous-rotation conveyors and two positional servos."""
    def __init__(self):
        if _USE_REAL_SERVOS:
            self.conveyor_1 = ContinuousServo(
                CONVEYOR_1_PIN,
                initial_value=0,
                min_pulse_width=MIN_PULSE_WIDTH,
                max_pulse_width=MAX_PULSE_WIDTH,
            )
            self.conveyor_2 = ContinuousServo(
                CONVEYOR_2_PIN,
                initial_value=0,
                min_pulse_width=MIN_PULSE_WIDTH,
                max_pulse_width=MAX_PULSE_WIDTH,
            )
            self.stopper = AngularServo(
                STOPPER_PIN,
                min_angle=0,
                max_angle=180,
                min_pulse_width=MIN_PULSE_WIDTH,
                max_pulse_width=MAX_PULSE_WIDTH,
            )
            self.sorter = AngularServo(
                SORTER_PIN,
                min_angle=0,
                max_angle=180,
                min_pulse_width=MIN_PULSE_WIDTH,
                max_pulse_width=MAX_PULSE_WIDTH,
            )
            self.stopper.angle = 180
            self.sorter.angle = 90
        else:
            print(
                "[MockServos] Initialized: conveyors BCM 18/12, "
                "stopper BCM 13, sorter BCM 19"
            )

    def start_conveyors(self, c1_speed=-1.0, c2_speed=-1.0):
        print(f"[Servos] Starting conveyors: {c1_speed}, {c2_speed}")
        if _USE_REAL_SERVOS:
            self.conveyor_1.value = c1_speed
            self.conveyor_2.value = c2_speed

    def stop_conveyors(self):
        print("[Servos] Stopping conveyors")
        if _USE_REAL_SERVOS:
            self.conveyor_1.value = 0
            self.conveyor_2.value = 0

    def trigger_stopper(self):
        print("[Servos] Moving stopper down and back up")
        if _USE_REAL_SERVOS:
            self.stopper.angle = 0
        time.sleep(1.0)
        if _USE_REAL_SERVOS:
            self.stopper.angle = 180
        time.sleep(0.5)

    def sort_seed(self, status):
        if status in ("healthy", "left"):
            angle = 0
            destination = "healthy/left"
        elif status in ("unhealthy", "right"):
            angle = 180
            destination = "unhealthy/right"
        else:
            angle = 90
            destination = "center"

        print(f"[Servos] Sorting {status} seed toward {destination}")
        if _USE_REAL_SERVOS:
            self.sorter.angle = angle
        time.sleep(1.2)
        if _USE_REAL_SERVOS:
            self.sorter.angle = 90
        time.sleep(0.5)

    def detach(self):
        if _USE_REAL_SERVOS:
            self.stop_conveyors()
            for servo in (
                self.conveyor_1,
                self.conveyor_2,
                self.stopper,
                self.sorter,
            ):
                servo.detach()
        print("[Servos] Detached")