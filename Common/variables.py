import json
import os

# File path for settings.json
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# Default Variables
# Temperatures
temp_BK = 100
temp_MLT = 68
temp_HLT = 70

temp_progress_BK = 0
temp_progress_HLT = 0

# Efficiency
efficiency_BK = 100
efficiency_HLT = 100
BK_PWM = None
HLT_PWM = None

# REG values
temp_REG_BK = 85
temp_REG_HLT = 70
set_temp_reached_BK = False
set_temp_reached_HLT = False

# Pump speeds
pump_speed_P1 = 100
pump_speed_P2 = 100
P1_PWM = None
P2_PWM = None

# Active Units
STATE = {
    "BK_ON": False,
    "HLT_ON": False,
    "P1_ON": False,
    "P2_ON": False,
}

active_variable = None

#ChatGPT API
talking_with_chat = False

def initialize_variables_from_settings():
    """Load settings from the JSON file and update variables."""
    global temp_BK, temp_HLT, temp_REG_BK, temp_REG_HLT
    global efficiency_BK, efficiency_HLT, pump_speed_P1, pump_speed_P2

    if not os.path.exists(SETTINGS_FILE):
        raise FileNotFoundError(f"Settings file not found at {SETTINGS_FILE}")

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    # Update variables from settings
    temp_REG_BK = settings.get("REG starting temperature BK", temp_REG_BK)
    temp_REG_HLT = settings.get("REG starting temperature HLT", temp_REG_HLT)
    efficiency_BK = settings.get("starting efficiency BK", efficiency_BK)
    efficiency_HLT = settings.get("starting efficiency HLT", efficiency_HLT)
    pump_speed_P1 = settings.get("starting efficiency P1", pump_speed_P1)
    pump_speed_P2 = settings.get("starting efficiency P2", pump_speed_P2)

# Initialize variables at the time of import
initialize_variables_from_settings()
