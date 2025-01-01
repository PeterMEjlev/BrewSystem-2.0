# graphscreen_static_gui.py
from Common.utils import create_image, create_label
import Common.gui_constants as gui_constants
from PyQt5.QtCore import Qt
import os 

def initialize_static_images(parent_widget, assets_path):
    """
    Initialize static images on the GUI.
    """
    return {
        # Dropshadows
        'IMG_Dropshadow_Sidebar': create_image(
            parent_widget, os.path.join(assets_path, "Dropshadow_Sidebar.png"), center=gui_constants.IMG_DROPSHADOWS_COORDINATES
        ),

        # Sidebar and Title
        'IMG_Sidebar': create_image(parent_widget, "Sidebar.png", center=(0, 0)),
        'IMG_Title': create_image(parent_widget, os.path.join(assets_path, "Banner_Title.png"), center=(0, 0)),
        'IMG_Sidebar_Active_Button': create_image(parent_widget, os.path.join(assets_path, "Sidebar_Active_Button.png"), center=gui_constants.IMG_SIDEBAR_ACTIVE_BUTTON_GRAPHS),
        'IMG_Sidebar_Icon_Home': create_image(parent_widget, os.path.join(assets_path, "Icon_Home.png"), center=gui_constants.IMG_SIDEBAR_ICON_HOME),
        'IMG_Sidebar_Icon_Graph': create_image(parent_widget, os.path.join(assets_path, "Icon_Graph.png"), center=gui_constants.IMG_SIDEBAR_ICON_GRAPHS),
        'IMG_Sidebar_Konfus_Logo': create_image(parent_widget, os.path.join(assets_path, "Konfus_Logo.png"), center=gui_constants.IMG_KONFUS_LOGO),
    }

def initialize_static_text(parent_widget):
    """
    Initialize static text on the GUI.
    """
    return {
        # Title
        'TXT_Title': create_label(parent_widget, "BrewSystem 2.0", color='white', size=gui_constants.TXT_TITLE_SIZE, center=gui_constants.TXT_TITLE_COORDINATES, width = 500),
        'TXT_SIDEBAR_HOME': create_label(parent_widget, "Overview", color='white', size=gui_constants.TXT_SIDEBAR_TEXT_SIZE, center=gui_constants.TXT_SIDEBAR_TEXT_HOME,  alignment=Qt.AlignLeft),
        'TXT_SIDEBAR_GRAPHS': create_label(parent_widget, "Graphs", color='white', size=gui_constants.TXT_SIDEBAR_TEXT_SIZE, center=gui_constants.TXT_SIDEBAR_TEXT_GRAPHS,  alignment=Qt.AlignLeft),
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
    # Pass both parent_widget and assets_path to initialize_static_images
    static_images = initialize_static_images(parent_widget, assets_path)
    static_text = initialize_static_text(parent_widget)

    # Merge dictionaries and return
    return {**static_images, **static_text}
