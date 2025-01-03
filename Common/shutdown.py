from PyQt5.QtWidgets import QApplication
from Common.utils_rpi import set_gpio_low, stop_pwm_signal
from Common.constants_rpi import RPI_GPIO_PIN_BK, RPI_GPIO_PIN_HLT, RPI_GPIO_PWN_BK, RPI_GPIO_PWN_HLT
import Common.variables as variables

def perform_shutdown():
    """
    Central shutdown function to ensure all GPIO and PWM signals are properly turned off
    before quitting the application.
    """
    print("Performing shutdown...")
    
    # Turn off GPIO pins for BK and HLT
    set_gpio_low(RPI_GPIO_PIN_BK)
    set_gpio_low(RPI_GPIO_PIN_HLT)
    
    # Stop PWM signals for BK and HLT
    if variables.BK_PWM:
        stop_pwm_signal(variables.BK_PWM)
        variables.BK_PWM = None
    
    if variables.HLT_PWM:
        stop_pwm_signal(variables.HLT_PWM)
        variables.HLT_PWM = None

    print("All GPIO and PWM signals have been reset.")

    # Quit the application
    QApplication.quit()
