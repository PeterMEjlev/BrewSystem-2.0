# utils.py

try:
    import RPi.GPIO as GPIO
    IS_RPI = True
    print("Running on Raspberry Pi with GPIO support.")
except ImportError:
    IS_RPI = False
    print("Running on non-Raspberry Pi platform. GPIO functionality will be disabled.")


