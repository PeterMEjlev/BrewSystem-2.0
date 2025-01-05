# utils_rpi.py
from Common.config import IS_RPI
import random
import Common.utils_rpi as utils_rpi

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
            GPIO.output(pin_number, GPIO.HIGH)
            print(f"GPIO pin {pin_number} set to HIGH.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to HIGH: {e}")
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
            GPIO.output(pin_number, GPIO.LOW)
            print(f"GPIO pin {pin_number} set to LOW.")
        except Exception as e:
            print(f"An error occurred while setting GPIO pin {pin_number} to LOW: {e}")
    else:
        print(f"GPIO pin {pin_number} set to LOW (simulated).")

def set_pwm_signal(pin_number, frequency, duty_cycle):
    """
    Turns on a PWM signal on a specified GPIO pin on the Raspberry Pi.

    Args:
        pin_number (int): The GPIO pin number to use for PWM.
        frequency (float): The frequency of the PWM signal in Hz.
        duty_cycle (float): The duty cycle of the PWM signal as a percentage (0.0 to 100.0).
    """
    if IS_RPI:
        try:
            # Use Broadcom pin numbering
            GPIO.setmode(GPIO.BCM)

            # Set up the pin as an output
            GPIO.setup(pin_number, GPIO.OUT)

            # Initialize PWM on the pin with the specified frequency
            pwm = GPIO.PWM(pin_number, frequency)

            # Start PWM with the specified duty cycle
            pwm.start(duty_cycle)

            print(f"PWM started on GPIO pin {pin_number} with frequency {frequency}Hz and duty cycle {duty_cycle}%.")

            return pwm  # Return the PWM object to allow further control (e.g., stop, change frequency/duty cycle)
        except Exception as e:
            print(f"An error occurred while starting PWM on GPIO pin {pin_number}: {e}")
    else:
        print(f"PWM started on GPIO pin {pin_number} with frequency {frequency}Hz and duty cycle {duty_cycle}% (simulated).")

def stop_pwm_signal(pwm):
    """
    Stops the PWM signal on the specified PWM object.

    Args:
        pwm (GPIO.PWM): The PWM object to stop.
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

    Args:
        pwm (GPIO.PWM): The PWM object to modify.
        duty_cycle (float): The new duty cycle as a percentage (0.0 to 100.0).
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
            return random.uniform(35.0, 102.0) # Replace with actual code to read the DS18B20 sensor
        except Exception as e:
            print(e)
    else:
        return random.uniform(35.0, 102.0)  # Simulated temperature
    
def initialize_gpio():
    """
    Initializes the GPIO pins for the Raspberry Pi.
    Sets the GPIO mode and configures the necessary pins as outputs.
    """
    if IS_RPI:
        try:
            # Set Broadcom numbering mode
            GPIO.setmode(GPIO.BCM)

            # Setup designated GPIO pins as outputs
            GPIO.setup(utils_rpi.RPI_GPIO_PIN_BK, GPIO.OUT)
            GPIO.setup(utils_rpi.RPI_GPIO_PIN_HLT, GPIO.OUT)
            GPIO.setup(utils_rpi.RPI_GPIO_PWN_BK, GPIO.OUT)
            GPIO.setup(utils_rpi.RPI_GPIO_PWN_HLT, GPIO.OUT)
            GPIO.setup(utils_rpi.RPI_GPIO_PIN_P1, GPIO.OUT)
            GPIO.setup(utils_rpi.RPI_GPIO_PIN_P2, GPIO.OUT)

            print("GPIO pins initialized.")
        except Exception as e:
            print(f"An error occurred during GPIO initialization: {e}")
    else:
        print("GPIO initialization skipped (simulated mode).")
