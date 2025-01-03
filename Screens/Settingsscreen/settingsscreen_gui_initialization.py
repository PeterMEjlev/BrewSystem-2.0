# settingsscreen_gui_initialization.py
from Screens.Settingsscreen.settingsscreen_static_gui import initialize_static_elements
import PyQt5.QtWidgets as QtWidgets
from Common.utils import create_button
import Common.constants_gui as constants_gui
from PyQt5.QtCore import QTimer

def initialize_gui_elements(parent_widget, assets_path):
    """
    Initializes GUI elements for the SettingsScreen.

    Parameters:
    - parent_widget: The widget to which the elements are added.
    - assets_path: The path to the assets directory.
    """
    if not assets_path:
        raise ValueError("Assets path is not set. Ensure `assets_path` is correctly initialized.")

    # Initialize static elements
    parent_widget.static_elements = initialize_static_elements(parent_widget, assets_path)

    # Explicitly show all elements
    for key, element in parent_widget.static_elements.items():
        element.show()

    # Initialize buttons
    parent_widget.buttons = initialize_buttons(parent_widget)


def initialize_buttons(parent_widget):
    """
    Initializes buttons for the SettingsScreen.

    Parameters:
    - parent_widget: The widget to which the button is added.

    Returns:
    A dictionary containing the button(s).
    """
    buttons = {
        'BTN_close_settings_window': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_COORDINATES,  # Example position
            size=constants_gui.BTN_SIDEBAR_MENU,  # Example size
            on_normal_click=parent_widget.close,  # Close the parent widget
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_open_graphs_window': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_GRAPHS_COORDINATES,  # Example position
            size=constants_gui.BTN_SIDEBAR_MENU,  # Example size
            on_normal_click=lambda: (
                parent_widget.open_graph_screen(),
                QTimer.singleShot(100, parent_widget.close)
            ),         
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_quit': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_QUIT_COORDINATES,
            size=constants_gui.BTN_QUIT,
            on_normal_click=lambda: QtWidgets.QApplication.quit(),
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
    }

    # Show the button explicitly
    for button in buttons.values():
        button.show()

    return buttons
