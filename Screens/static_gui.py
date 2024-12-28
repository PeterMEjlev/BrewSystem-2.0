from Common.utils import create_image, create_label
import Common.constants as constants
from PyQt5.QtCore import Qt

def initialize_static_images(parent_widget):
    """
    Initialize static images on the GUI.
    """
    return {
        # Dropshadows
        'IMG_Dropshadows': create_image(parent_widget, "Dropshadows.png", location=constants.IMG_DROPSHADOWS_COORDINATES),
        
        # Sidebar and Title
        'IMG_Title': create_image(parent_widget, "Banner_Title.png", location=(0, 0)),

        # Pots
        'IMG_Pot_BK_Off_Background': create_image(parent_widget, "Pot_Off_Background.png", location=constants.IMG_POT_BK_COORDINATES),
        'IMG_Pot_BK_On_Background': create_image(parent_widget, "Pot_On_Background.png", location=constants.IMG_POT_BK_COORDINATES), # Hidden     
        'IMG_Pot_BK_On_Foreground': create_image(parent_widget, "Pot_On_Foreground.png", location=constants.IMG_POT_BK_COORDINATES), # Hidden 
        'IMG_Pot_BK': create_image(parent_widget, "Pot_Outline.png", location=constants.IMG_POT_BK_COORDINATES),
        
        'IMG_Pot_MLT_Off_Background': create_image(parent_widget, "Pot_Off_Background.png", location=constants.IMG_POT_MLT_COORDINATES),        
        'IMG_Pot_MLT_On_Background': create_image(parent_widget, "Pot_On_Background.png", location=constants.IMG_POT_MLT_COORDINATES), # Hidden     
        'IMG_Pot_MLT_On_Foreground': create_image(parent_widget, "Pot_On_Foreground.png", location=constants.IMG_POT_MLT_COORDINATES), # Hidden 
        'IMG_Pot_MLT': create_image(parent_widget, "Pot_Outline.png", location=constants.IMG_POT_MLT_COORDINATES),
        
        'IMG_Pot_HLT_Off_Background': create_image(parent_widget, "Pot_Off_Background.png", location=constants.IMG_POT_HLT_COORDINATES),  
        'IMG_Pot_HLT_On_Background': create_image(parent_widget, "Pot_On_Background.png", location=constants.IMG_POT_HLT_COORDINATES), # Hidden     
        'IMG_Pot_HLT_On_Foreground': create_image(parent_widget, "Pot_On_Foreground.png", location=constants.IMG_POT_HLT_COORDINATES), # Hidden       
        'IMG_Pot_HLT': create_image(parent_widget, "Pot_Outline.png", location=constants.IMG_POT_HLT_COORDINATES),

        # Pipes and Reg Boxes
        'IMG_Pipes': create_image(parent_widget, "Pipes.png", location=constants.IMG_PIPES_COORDINATES),
        'IMG_Reg_BK': create_image(parent_widget, "Reg_Box.png", location=constants.IMG_REG_BOX_BK_COORDINATES),
        'IMG_Reg_HLT': create_image(parent_widget, "Reg_Box.png", location=constants.IMG_REG_BOX_HLT_COORDINATES),

        # Coil and Heating Elements
        'IMG_Coil': create_image(parent_widget, "Coil.png", location=constants.IMG_COIL_COORDINATES),
        'IMG_Heating_Element_BK': create_image(parent_widget, "Heating_Element.png", location=constants.IMG_HEATING_ELEMENT_BK_COORDINATES),
        'IMG_Heating_Element_HLT': create_image(parent_widget, "Heating_Element.png", location=constants.IMG_HEATING_ELEMENT_HLT_COORDINATES),

        # Pump Boxes
        'IMG_Pump_Box_P1': create_image(parent_widget, "Pump_Box.png", location=constants.IMG_PUMP_BOX_P1_COORDINATES),
        'IMG_Pump_Box_P2': create_image(parent_widget, "Pump_Box.png", location=constants.IMG_PUMP_BOX_P2_COORDINATES),

        # Selection Text
        'IMG_BK_Selected': create_image(parent_widget, "TXT_BK_Selected.png", location=constants.TXT_BK_SELECTED),
        'IMG_HLT_Selected': create_image(parent_widget, "TXT_HLT_Selected.png", location=constants.TXT_HLT_SELECTED),
        'IMG_REGBK_Selected': create_image(parent_widget, "TXT_REG_Selected.png", location=constants.TXT_REGBK_SELECTED),
        'IMG_REGHLT_Selected': create_image(parent_widget, "TXT_REG_Selected.png", location=constants.TXT_REGHLT_SELECTED),
        'IMG_P1_Selected': create_image(parent_widget, "TXT_P1_Selected.png", location=constants.TXT_P1_SELECTED),
        'IMG_P2_Selected': create_image(parent_widget, "TXT_P2_Selected.png", location=constants.TXT_P2_SELECTED),
    }

def initialize_static_text(parent_widget):
    """
    Initialize static text on the GUI.
    """
    return {
        # Title
        'TXT_Title': create_label(parent_widget, "BrewSystem 2.0", color='white', size=constants.TXT_TITLE_SIZE, location=constants.TXT_TITLE_COORDINATES),

        # Pot Names
        'TXT_POT_NAME_BK': create_label(parent_widget, "BK", color='white', size=constants.TXT_POT_NAMES_SIZE, location=constants.TXT_POT_NAMES_BK_COORDINATES),
        'TXT_POT_NAME_MLT': create_label(parent_widget, "MLT", color='white', size=constants.TXT_POT_NAMES_SIZE, location=constants.TXT_POT_NAMES_MLT_COORDINATES),
        'TXT_POT_NAME_HLT': create_label(parent_widget, "HLT", color='white', size=constants.TXT_POT_NAMES_SIZE, location=constants.TXT_POT_NAMES_HLT_COORDINATES),

        # Slider Min/Max
        'TXT_Slider_0': create_label(parent_widget, "0", color='white', size=constants.TXT_SLIDER_MINMAX_SIZE, location=constants.TXT_SLIDER_MIN_COORDINATES),
        'TXT_Slider_100': create_label(parent_widget, "100", color='white', size=constants.TXT_SLIDER_MINMAX_SIZE, location=constants.TXT_SLIDER_MAX_COORDINATES),

        # Pump Names
        'TXT_P1': create_label(parent_widget, "P1", color='white', size=constants.TXT_SLIDER_VALUE_SIZE, location=constants.TXT_P1_COORDINATES),
        'TXT_P2': create_label(parent_widget, "P2", color='white', size=constants.TXT_SLIDER_VALUE_SIZE, location=constants.TXT_P2_COORDINATES),

        # Reg Labels
        'TXT_REG_BK': create_label(parent_widget, "REG", color='white', size=constants.TXT_REG_SIZE, location=constants.TXT_REG_BK_COORDINATES),
        'TXT_REG_HLT': create_label(parent_widget, "REG", color='white', size=constants.TXT_REG_SIZE, location=constants.TXT_REG_HLT_COORDINATES),
        
        # Reg Values
        'TXT_REG_BK_VALUE': create_label(parent_widget, "0", color='white', size=constants.TXT_REG_VALUE_SIZE, location=constants.TXT_REG_BK_VALUE_COORDINATES, alignment=Qt.AlignCenter),
        'TXT_REG_HLT_VALUE': create_label(parent_widget, "0", color='white', size=constants.TXT_REG_VALUE_SIZE, location=constants.TXT_REG_HLT_VALUE_COORDINATES, alignment=Qt.AlignCenter),

    }

def initialize_static_elements(parent_widget, assets_path):
    """
    Initialize all static GUI elements and combine them into a single dictionary.

    Parameters:
    parent_widget (QWidget): The widget to which static elements will be added.
    assets_path (str): The base path for the assets directory.

    Returns:
    dict: A dictionary containing references to all the static elements.
    """
    # Initialize images and text separately
    static_images = initialize_static_images(parent_widget)
    static_text = initialize_static_text(parent_widget)

    # Merge dictionaries and return
    return {**static_images, **static_text}
