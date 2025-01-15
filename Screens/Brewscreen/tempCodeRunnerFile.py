from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
import Common.constants
from Common.utils import create_slider, create_button, toggle_variable, set_label_text_color
from Common.utils_rpi import set_pwm_signal, stop_pwm_signal, create_software_pwm
from Common.variables import STATE
from Common.constants import SLIDER_PAGESTEP
import Common.constants_rpi as constants_rpi
import Common.constants_gui as constants_gui
import Common.variables as variables
from Common.shutdown import perform_shutdown