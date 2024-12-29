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
        'TXT_TEMP_BK': create_label(parent_widget, str(variables.temp_BK), color='white', size=constants.TXT_POT_TEMPERATURES_SIZE, location=constants.TXT_TEMP_BK_COORDINATES),

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