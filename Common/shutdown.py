from PyQt5.QtWidgets import QApplication
from Common.utils_rpi import set_gpio_low, stop_pwm_signal
import Common.constants_rpi as constants_rpi
from Common.config import IS_RPI
import Common.variables as variables


if (IS_RPI):
    import RPi.GPIO as GPIO

def perform_shutdown():
    """
    Central shutdown function to ensure all GPIO and PWM signals are properly turned off
    before quitting the application.
    """
    print("Performing shutdown...")

    # Turn off GPIO pins
    set_gpio_low(constants_rpi.RPI_GPIO_PIN_BK)
    set_gpio_low(constants_rpi.RPI_GPIO_PIN_HLT)
    set_gpio_low(constants_rpi.RPI_GPIO_PIN_P1)
    set_gpio_low(constants_rpi.RPI_GPIO_PIN_P2)

    # Stop PWM signals
    if variables.BK_PWM:
        stop_pwm_signal(variables.BK_PWM)
        variables.BK_PWM = None

    if variables.HLT_PWM:
        stop_pwm_signal(variables.HLT_PWM)
        variables.HLT_PWM = None

    # Cleanup GPIO
    if IS_RPI:
        GPIO.cleanup()
        print("GPIO cleaned up.")

    print("Shutdown complete.")
    # Quit the application
    QApplication.quit()
