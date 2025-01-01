# utils_rpi.py
from Common.config import IS_RPI

if (IS_RPI):
    import RPi.GPIO as GPIO

def set_gpio_high(pin_number):
    """
    Sets a GPIO pin to HIGH (3.3V) on the Raspberry Pi.

    Args:
        pin_number (int): The GPIO pin number to set to HIGH.
    """
    if IS_RPI:
        try:
            # Use Broadcom pin numbering
            GPIO.setmode(GPIO.BCM)

            # Set up the pin as an output
            GPIO.setup(pin_number, GPIO.OUT)

            # Set the pin to HIGH
            GPIO.output(pin_number, GPIO.HIGH)

            print(f"GPIO pin {pin_number} set to HIGH.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to HIGH: {e}")
        finally:
            # It's good practice to clean up resources
            GPIO.cleanup(pin_number)
    else:
        print(f"GPIO pin {pin_number} set to HIGH (simulated).")

def set_gpio_low(pin_number):
    """
    Sets a GPIO pin to LOW (0V) on the Raspberry Pi.

    Args:
        pin_number (int): The GPIO pin number to set to LOW.
    """
    if IS_RPI:
        try:
            # Use Broadcom pin numbering
            GPIO.setmode(GPIO.BCM)

            # Set up the pin as an output
            GPIO.setup(pin_number, GPIO.OUT)

            # Set the pin to LOW
            GPIO.output(pin_number, GPIO.LOW)

            print(f"GPIO pin {pin_number} set to LOW.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to LOW: {e}")
        finally:
            # It's good practice to clean up resources
            GPIO.cleanup(pin_number)
    else:
        print(f"GPIO pin {pin_number} set to LOW (simulated).")