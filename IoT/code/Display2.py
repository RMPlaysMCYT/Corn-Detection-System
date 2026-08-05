import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Initialize I2C interface using Blinka translation layer
i2c = busio.I2C(board.SCL, board.SDA)

# Define screen dimensions (most common size is 128x64)
WIDTH = 128
HEIGHT = 64
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Clear display
oled.fill(0)
oled.show()

# Create a blank image canvas to draw on (1-bit pixels)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a default text font
font = ImageFont.load_default()

# Draw text onto the blank canvas canvas
draw.text((0, 0), "Raspberry Pi 5", font=font, fill=255)
draw.text((0, 20), "Python Display OK!", font=font, fill=255)

# Render the canvas image on the physical OLED panel
oled.image(image)
oled.show()