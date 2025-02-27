# graphscreen_static_gui.py
from Common.utils import create_image, create_label
import Common.constants_gui as constants_gui
from PyQt5.QtCore import Qt
import os 

def initialize_static_images(parent_widget, assets_path):
    """
    Initialize static images on the GUI.
    """
    return {
        # Dropshadows
        'IMG_Dropshadow_Sidebar': create_image(
            parent_widget, os.path.join(assets_path, "Dropshadow_Sidebar.png"), center=constants_gui.IMG_DROPSHADOWS_COORDINATES
        ),

        # Sidebar and Title
        'IMG_Sidebar': create_image(parent_widget, "Sidebar.png", center=(0, 0)),
        'IMG_Title': create_image(parent_widget, os.path.join(assets_path, "Banner_Title.png"), center=(0, 0)),
        'IMG_Sidebar_Active_Button': create_image(parent_widget, os.path.join(assets_path, "Sidebar_Active_Button.png"), center=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_GRAPHS_COORDINATES),
        'IMG_Sidebar_Icon_Home': create_image(parent_widget, os.path.join(assets_path, "Icon_Home.png"), center=constants_gui.IMG_SIDEBAR_ICON_HOME),
        'IMG_Sidebar_Icon_Graph': create_image(parent_widget, os.path.join(assets_path, "Icon_Graph.png"), center=constants_gui.IMG_SIDEBAR_ICON_GRAPHS),
        'IMG_Sidebar_Icon_Settings': create_image(parent_widget, "Icon_Settings.png", center=constants_gui.IMG_SIDEBAR_ICON_SETTINGS),
        'IMG_Sidebar_Voicelines_Grey': create_image(parent_widget, "Voicelines_Grey.png", center=constants_gui.IMG_VOICELINES),
        'IMG_Sidebar_Konfus_Logo': create_image(parent_widget, os.path.join(assets_path, "Konfus_Logo.png"), center=constants_gui.IMG_KONFUS_LOGO),

        # Graph Buttons
        'IMG_Y_Zoom_In': create_image(parent_widget, os.path.join(assets_path, "Zoom_In.png"), center=(constants_gui.BTN_GRAPH_Y_ZOOM_IN_COORDINATES[0]+16,constants_gui.BTN_GRAPH_Y_ZOOM_IN_COORDINATES[1]+16)),
        'IMG_Y_Zoom_Out': create_image(parent_widget, os.path.join(assets_path, "Zoom_Out.png"), center=(constants_gui.BTN_GRAPH_Y_ZOOM_OUT_COORDINATES[0]+16,constants_gui.BTN_GRAPH_Y_ZOOM_OUT_COORDINATES[1]+16)),

        'IMG_X_Zoom_In': create_image(parent_widget, os.path.join(assets_path, "Zoom_In.png"), center=(constants_gui.BTN_GRAPH_X_ZOOM_IN_COORDINATES[0]+16,constants_gui.BTN_GRAPH_X_ZOOM_IN_COORDINATES[1]+16)),
        'IMG_X_Zoom_Out': create_image(parent_widget, os.path.join(assets_path, "Zoom_Out.png"), center=(constants_gui.BTN_GRAPH_X_ZOOM_OUT_COORDINATES[0]+16,constants_gui.BTN_GRAPH_X_ZOOM_OUT_COORDINATES[1]+16)),

        'IMG_Zoom_Auto': create_image(parent_widget, os.path.join(assets_path, "Zoom_Auto.png"), center=(constants_gui.BTN_GRAPH_ZOOM_AUTO_COORDINATES[0]+16,constants_gui.BTN_GRAPH_ZOOM_AUTO_COORDINATES[1]+16)),

        'IMG_Legend_BK': create_image(parent_widget, os.path.join(assets_path, "Legend_BK.png"), center=constants_gui.IMG_LEGEND_BK_COORDINATES),
        'IMG_Legend_MLT': create_image(parent_widget, os.path.join(assets_path, "Legend_MLT.png"), center=constants_gui.IMG_LEGEND_MLT_COORDINATES),
        'IMG_Legend_HLT': create_image(parent_widget, os.path.join(assets_path, "Legend_HLT.png"), center=constants_gui.IMG_LEGEND_HLT_COORDINATES),


    }

def initialize_static_text(parent_widget):
    """
    Initialize static text on the GUI.
    """
    return {
        # Title
        'TXT_Title': create_label(parent_widget, "BrewSystem 2.0", color='white', size=constants_gui.TXT_TITLE_SIZE, center=constants_gui.TXT_TITLE_COORDINATES, width = 500),
        'TXT_SIDEBAR_HOME': create_label(parent_widget, "Overview", color='white', size=constants_gui.TXT_SIDEBAR_TEXT_SIZE, center=constants_gui.TXT_SIDEBAR_TEXT_HOME,  alignment=Qt.AlignLeft),
        'TXT_SIDEBAR_GRAPHS': create_label(parent_widget, "Graphs", color='white', size=constants_gui.TXT_SIDEBAR_TEXT_SIZE, center=constants_gui.TXT_SIDEBAR_TEXT_GRAPHS,  alignment=Qt.AlignLeft),
        'TXT_SIDEBAR_SETTINGS': create_label(parent_widget, "Settings", color='white', size=constants_gui.TXT_SIDEBAR_TEXT_SIZE, center=constants_gui.TXT_SIDEBAR_TEXT_SETTINGS,  alignment=Qt.AlignLeft),

        # Quit
        'TXT_EXIT': create_label(parent_widget, "exit", color=constants_gui.TXT_EXIT_COLOUR, size=constants_gui.TXT_EXIT_SIZE, center=constants_gui.TXT_EXIT_COORDINATES),
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
