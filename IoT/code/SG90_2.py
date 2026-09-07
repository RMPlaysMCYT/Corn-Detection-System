from time import sleep
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

# Initialize pigpio pin factory for Raspberry Pi 5 PWM support
factory = PiGPIOFactory()

# Setup servo on GPIO 12 with standard SG90 pulse widths (0.5ms to 2.5ms)
servo = Servo(12, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000, pin_factory=factory)

try:
  while True:
    print('Moving to 0 degrees (min)')
    servo.min()
    sleep(2)

    print('Moving to 90 degrees (mid)')
    servo.mid()
    sleep(2)

    print('Moving to 180 degrees (max)')
    servo.max()
    sleep(2)

except KeyboardInterrupt:
  print('Program stopped by user')
  servo.value = None