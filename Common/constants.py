# constants.py
import os

# Screen dimensions
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Colors
BACKGROUND_COLOR = "#3E3E3F"

# Slider configuration
SLIDER_MIN = 0
SLIDER_MAX = 100
SLIDER_PAGESTEP = 1

# Thermometer configuration
THERMOMETER_READ_WAIT_TIME = 1000  # Time in milliseconds
TEMP_REACHED_THRESHOLD = 1  # Temperature threshold for reaching target

# Button visibility
BTN_INVISIBILITY = True

GRAPH_LINE_WIDTH = 4

#Soundfiles folder
SOUNDFILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "Soundfiles"))


