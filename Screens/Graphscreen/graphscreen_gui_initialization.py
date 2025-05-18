import Common.constants
from Screens.Graphscreen.graphscreen_static_gui import initialize_static_elements
from Screens.Graphscreen.graphscreen_dynamic_gui import initialize_dynamic_elements
from Common.utils import create_button, set_opacity
import Common.constants_gui as constants_gui
from PyQt5.QtCore import QTimer
from Common.shutdown import perform_shutdown


def initialize_gui_elements(parent_widget, assets_path):
    """
    Initializes GUI elements for the GraphScreen.

    Parameters:
    - parent_widget: The widget to which the elements are added.
    - assets_path: The path to the assets directory.
    """
    if not assets_path:
        raise ValueError("Assets path is not set. Ensure `assets_path` is correctly initialized.")

    # Initialize static elements
    parent_widget.static_elements = initialize_static_elements(parent_widget, assets_path)

    # Initialize dynamic text elements (e.g., current pot temperatures)
    parent_widget.dynamic_elements = initialize_dynamic_elements(parent_widget, assets_path)

    # Explicitly show all static elements
    for element in parent_widget.static_elements.values():
        element.show()

    # Explicitly show all dynamic elements
    for element in parent_widget.dynamic_elements.values():
        element.show()

    # Initialize buttons
    parent_widget.buttons = initialize_buttons(parent_widget)


def initialize_buttons(parent_widget):
    """
    Initializes buttons for the GraphScreen.

    Parameters:
    - parent_widget: The widget to which the button is added.

    Returns:
    A dictionary containing the button(s).
    """
    buttons = {
        'BTN_close_graph_window': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_COORDINATES,
            size=constants_gui.BTN_SIDEBAR_MENU,
            on_normal_click=parent_widget.close,
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_open_settings_window': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_SETTINGS_COORDINATES,
            size=constants_gui.BTN_SIDEBAR_MENU,
            on_normal_click=lambda: (
                parent_widget.open_settings_screen(),
                QTimer.singleShot(100, parent_widget.close)
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_quit': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_QUIT_COORDINATES,
            size=constants_gui.BTN_QUIT,
            on_normal_click=lambda: perform_shutdown(),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_y_zoom_in': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_Y_ZOOM_IN_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_in(axis="y"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_y_zoom_out': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_Y_ZOOM_OUT_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_out(axis="y"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_x_zoom_in': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_X_ZOOM_IN_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_in(axis="x"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_x_zoom_out': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_X_ZOOM_OUT_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_out(axis="x"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_zoom_auto': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_ZOOM_AUTO_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.enable_auto_range(),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_bk_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_BK_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                    parent_widget.temperature_graph.toggle_line_visibility("bk"),
                    set_opacity(parent_widget, "bk")
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_mlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_MLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                parent_widget.temperature_graph.toggle_line_visibility("mlt"),
                set_opacity(parent_widget, "mlt")
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_hlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_HLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                parent_widget.temperature_graph.toggle_line_visibility("hlt"),
                set_opacity(parent_widget, "hlt")
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
    }

    # Show all buttons explicitly
    for btn in buttons.values():
        btn.show()

    return buttons
