# dynamic_gui.py
from Common.utils import create_label
import Common.variables as variables
import Common.constants_gui as constants_gui
from PyQt5.QtCore import Qt

def initialize_dynamic_text(parent_widget):
    """
    Initialize dynamic text on the GUI.
    """
    return {
        # Pot Temperatures
        'TXT_TEMP_BK': create_label(parent_widget, f"{variables.temp_BK}°", color='white', size=constants_gui.TXT_POT_TEMPERATURES_SIZE, center=constants_gui.TXT_TEMP_BK_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_TEMP_MLT': create_label(parent_widget, f"{variables.temp_MLT}°", color='white', size=constants_gui.TXT_POT_TEMPERATURES_SIZE, center=constants_gui.TXT_TEMP_MLT_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_TEMP_HLT': create_label(parent_widget, f"{variables.temp_HLT}°", color='white', size=constants_gui.TXT_POT_TEMPERATURES_SIZE, center=constants_gui.TXT_TEMP_HLT_COORDINATES, alignment=Qt.AlignCenter),

        # Reg Temperatures
        'TXT_TEMP_REG_BK': create_label(parent_widget, f"{variables.temp_REG_BK}°", color='white', size=constants_gui.TXT_REG_VALUE_SIZE, center=constants_gui.TXT_REG_BK_VALUE_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_TEMP_REG_HLT': create_label(parent_widget, f"{variables.temp_REG_HLT}°", color='white', size=constants_gui.TXT_REG_VALUE_SIZE, center=constants_gui.TXT_REG_HLT_VALUE_COORDINATES, alignment=Qt.AlignCenter),
    
        # Pump Speeds (PWM)
        'TXT_PUMP_SPEED_P1': create_label(parent_widget, f"{variables.pump_speed_P1}%", color='white', size=constants_gui.TXT_PUMP_SPEED_SIZE, center=constants_gui.TXT_P1_VALUE_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_PUMP_SPEED_P2': create_label(parent_widget, f"{variables.pump_speed_P2}%", color='white', size=constants_gui.TXT_PUMP_SPEED_SIZE, center=constants_gui.TXT_P2_VALUE_COORDINATES, alignment=Qt.AlignCenter),    
    }

def create_slider_value_label(parent_widget):
    """
    Create the slider value label.

    Parameters:
    parent_widget (QWidget): The widget to which the label will be added.

    Returns:
    QLabel: The created slider value label.
    """
    return create_label(
        parent_widget=parent_widget,
        text=str(),
        color='white',
        size=constants_gui.TXT_SLIDER_VALUE_SIZE,
        center=constants_gui.TXT_SLIDER_VALUE_COORDINATES
    )

def initialize_dynamic_elements(parent_widget, assets_path):
    """
    Initialize all dynamic GUI elements and combine them into a single dictionary.

    Parameters:
    parent_widget (QWidget): The widget to which dynamic elements will be added.
    assets_path (str): The base path for the assets directory.

    Returns:
    dict: A dictionary containing references to all the dynamic elements.
    """
    # Initialize images and text separately
    dynamic_text = initialize_dynamic_text(parent_widget)

    # Merge dictionaries and return
    return {**dynamic_text}
