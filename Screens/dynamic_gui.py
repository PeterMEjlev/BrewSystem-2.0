from Common.utils import create_label
import Common.variables as variables
import Common.constants as constants
from PyQt5.QtCore import Qt

def initialize_dynamic_text(parent_widget):
    """
    Initialize dynamic text on the GUI.
    """
    return {
        # Pot Temperatures
        'TXT_TEMP_BK': create_label(parent_widget, f"{variables.temp_BK}°", color='white', size=constants.TXT_POT_TEMPERATURES_SIZE, center=constants.TXT_TEMP_BK_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_TEMP_MLT': create_label(parent_widget, f"{variables.temp_MLT}°", color='white', size=constants.TXT_POT_TEMPERATURES_SIZE, center=constants.TXT_TEMP_MLT_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_TEMP_HLT': create_label(parent_widget, f"{variables.temp_HLT}°", color='white', size=constants.TXT_POT_TEMPERATURES_SIZE, center=constants.TXT_TEMP_HLT_COORDINATES, alignment=Qt.AlignCenter),
    }

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