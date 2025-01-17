# utils.py

try:
    import RPi.GPIO as GPIO
    IS_RPI = True
    print("Running on Raspberry Pi with GPIO support.")
except ImportError:
    IS_RPI = False
    print("Running on non-Raspberry Pi platform. GPIO functionality will be disabled.")

import psutil

def is_laptop():
    try:
        battery = psutil.sensors_battery()
        return battery is not None  # If a battery is detected, it's likely a laptop
    except AttributeError:
        return False  # psutil might not support battery detection on some systems

if is_laptop():
    print("Running on a laptop.")
    RUNNING_ON_LAPTOP = True
else:
    print("Not running on a laptop.")
    RUNNING_ON_LAPTOP = False
