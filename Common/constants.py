# constants.py
import os, json

# File path for settings.json
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

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
TEMP_REACHED_MARGIN = 10  # Temperature threshold for reaching target

# Button visibility
BTN_INVISIBILITY = True

GRAPH_LINE_WIDTH = 4

#Soundfiles folder
SOUNDFILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "Soundfiles"))


def initialize_constants_from_settings():
    """Load settings from the JSON file and update variables."""
    global TEMP_REACHED_MARGIN

    if not os.path.exists(SETTINGS_FILE):
        raise FileNotFoundError(f"Settings file not found at {SETTINGS_FILE}")

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    # Update variables from settings
    TEMP_REACHED_MARGIN = settings.get("target_temp_margin", TEMP_REACHED_MARGIN)

# Initialize variables at the time of import
initialize_constants_from_settings()