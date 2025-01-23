import json
import os



def get_setting(setting_name):
    SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

    if not os.path.exists(SETTINGS_FILE):
        raise FileNotFoundError(f"Settings file not found at {SETTINGS_FILE}")

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    setting_value = settings.get(setting_name)

    return setting_value
