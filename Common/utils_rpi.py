# utils_rpi.py
from Common.config import IS_RPI
import random
import Common.constants_rpi as constants_rpi

if IS_RPI:
    import RPi.GPIO as GPIO

def set_gpio_high(pin_number):
    """
    Sets a GPIO pin to HIGH (3.3V) on the Raspberry Pi.
    """
    if IS_RPI:
        try:
            GPIO.output(pin_number, GPIO.HIGH)
            print(f"GPIO pin {pin_number} set to HIGH.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to HIGH: {e}")
    else:
        print(f"GPIO pin {pin_number} set to HIGH (simulated).")

def set_gpio_low(pin_number):
    """
    Sets a GPIO pin to LOW (0V) on the Raspberry Pi.
    """
    if IS_RPI:
        try:
            GPIO.output(pin_number, GPIO.LOW)
            print(f"GPIO pin {pin_number} set to LOW.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to LOW: {e}")
    else:
        print(f"GPIO pin {pin_number} set to LOW (simulated).")

def set_pwm_signal(pin_number, frequency, duty_cycle):
    """
    Turns on a PWM signal on a specified GPIO pin on the Raspberry Pi.
    """
    if IS_RPI:
        try:
            GPIO.setup(pin_number, GPIO.OUT)  # Ensure the pin is set as an output
            pwm = GPIO.PWM(pin_number, frequency)  # Create PWM instance
            pwm.start(duty_cycle)  # Start PWM with duty cycle
            print(f"PWM started on GPIO pin {pin_number} with frequency {frequency}Hz and duty cycle {duty_cycle}%.")
            return pwm
        except Exception as e:
            print(f"An error occurred while starting PWM on GPIO pin {pin_number}: {e}")
    else:
        print(f"PWM started on GPIO pin {pin_number} with frequency {frequency}Hz and duty cycle {duty_cycle}% (simulated).")
        return None

def create_software_pwm(pin_number, frequency):
    """
    Creates a software PWM signal on a specified GPIO pin.

    Args:
        pin_number (int): The GPIO pin number to use for PWM.
        frequency (float): The frequency of the PWM signal in Hz.

    Returns:
        GPIO.PWM: A software PWM object.
    """
    if IS_RPI:
        try:
            GPIO.setup(pin_number, GPIO.OUT)  # Ensure the pin is set as an output
            pwm = GPIO.PWM(pin_number, frequency)  # Create software PWM instance
            print(f"Software PWM created on GPIO pin {pin_number} with frequency {frequency}Hz.")
            return pwm
        except Exception as e:
            print(f"An error occurred while creating software PWM on GPIO pin {pin_number}: {e}")
            return None
    else:
        print(f"Software PWM created on GPIO pin {pin_number} with frequency {frequency}Hz (simulated).")
        return None

def stop_pwm_signal(pwm):
    """
    Stops the PWM signal on the specified PWM object.
    """
    if IS_RPI and pwm:
        try:
            pwm.stop()
            print("PWM signal stopped.")
        except Exception as e:
            print(f"An error occurred while stopping the PWM signal: {e}")
    else:
        print("PWM signal stopped (simulated).")

def change_pwm_duty_cycle(pwm, duty_cycle):
    """
    Changes the duty cycle of an active PWM signal.
    """
    if IS_RPI and pwm:
        try:
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"{pwm} duty cycle changed to {duty_cycle}%.")
        except Exception as e:
            print(f"An error occurred while changing the {pwm} duty cycle: {e}")
    else:
        print(f"{pwm} duty cycle changed to {duty_cycle}% (simulated).")

def read_ds18b20(serial_code):
    if IS_RPI:
        try:
            return random.uniform(35.0, 102.0)  # Replace with actual code to read the DS18B20 sensor
        except Exception as e:
            print(e)
    else:
        return random.uniform(35.0, 102.0)  # Simulated temperature

def initialize_gpio():
    """
    Initializes the GPIO pins for the Raspberry Pi.
    Sets the GPIO mode and configures the necessary pins as outputs, defaulting them to LOW.
    """
    if IS_RPI:
        try:
            GPIO.setmode(GPIO.BCM)  # Set Broadcom numbering mode
            pins = [
                constants_rpi.RPI_GPIO_PIN_BK,
                constants_rpi.RPI_GPIO_PIN_HLT,
                constants_rpi.RPI_GPIO_PWN_BK,
                constants_rpi.RPI_GPIO_PWN_HLT,
                constants_rpi.RPI_GPIO_PIN_P1,
                constants_rpi.RPI_GPIO_PIN_P2
            ]

            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)  # Set pin as output
                GPIO.output(pin, GPIO.LOW)  # Default to LOW

            print("GPIO pins initialized and set to LOW.")
        except Exception as e:
            print(f"An error occurred during GPIO initialization: {e}")
    else:
        print("GPIO initialization skipped (simulated mode).")
