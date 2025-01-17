# utils.py

try:
    import RPi.GPIO as GPIO
    IS_RPI = True
    print("Running on Raspberry Pi with GPIO support.")
except ImportError:
    IS_RPI = False
    print("Running on non-Raspberry Pi platform. GPIO functionality will be disabled.")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Initialize QApplication to get screen resolution
app = QApplication([])
screen_geometry = app.primaryScreen().geometry()

# Check if the resolution is 1920x1080 or 16:9 aspect ratio
screen_width = screen_geometry.width()
screen_height = screen_geometry.height()
ASPECT_RATIO_16_9 = abs((screen_width / screen_height) - (16 / 9)) < 0.01  # Allowing for minor floating-point precision error

IS_WRONG_RESOLUTION = not (screen_width == 1920 and screen_height == 1080) and not ASPECT_RATIO_16_9

if IS_WRONG_RESOLUTION:
    print(f"Screen resolution {screen_width}x{screen_height} detected. IS_WRONG_RESOLUTION = True.")
else:
    print(f"Screen resolution {screen_width}x{screen_height} is valid. IS_WRONG_RESOLUTION = False.")
