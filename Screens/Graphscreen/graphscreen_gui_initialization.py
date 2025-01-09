from Screens.Graphscreen.graphscreen_static_gui import initialize_static_elements
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

    # Explicitly show all elements
    for key, element in parent_widget.static_elements.items():
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
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_COORDINATES,  # Example position
            size=constants_gui.BTN_SIDEBAR_MENU,  # Example size
            on_normal_click=parent_widget.close,  # Close the parent widget
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_open_settings_window': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_SETTINGS_COORDINATES,  # Example position
            size=constants_gui.BTN_SIDEBAR_MENU,  # Example size
            on_normal_click=lambda: (
                parent_widget.open_settings_screen(),
                QTimer.singleShot(100, parent_widget.close)
            ),         
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_quit': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_QUIT_COORDINATES,
            size=constants_gui.BTN_QUIT,
            on_normal_click=lambda: perform_shutdown(),
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_y_zoom_in': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_Y_ZOOM_IN_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_in(axis="y"),  # Updated
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_y_zoom_out': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_Y_ZOOM_OUT_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_out(axis="y"),  # Updated
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_x_zoom_in': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_X_ZOOM_IN_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_in(axis="x"),  # Updated
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_x_zoom_out': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_X_ZOOM_OUT_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.zoom_out(axis="x"),  # Updated
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_zoom_auto': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_ZOOM_AUTO_COORDINATES,
            size=constants_gui.BTN_GRAPH_ZOOM_SIZE,
            on_normal_click=lambda: parent_widget.temperature_graph.enable_auto_range(),  # Updated
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_bk_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_BK_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                    parent_widget.temperature_graph.toggle_line_visibility("bk"),
                    toggle_opacity(parent_widget, "bk")
            ),
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_mlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_MLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                parent_widget.temperature_graph.toggle_line_visibility("mlt"),
                toggle_opacity(parent_widget, "mlt")
            ),  
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_hlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_HLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: (
                parent_widget.temperature_graph.toggle_line_visibility("hlt"),  
                toggle_opacity(parent_widget, "hlt")
            ),
            on_long_click=None,
            invisible=constants_gui.BTN_INVISIBILITY
        ),
    }

    # Show the button explicitly
    for button in buttons.values():
        button.show()

    return buttons

def toggle_opacity(parent_widget, line_name):
    """
    Toggle the opacity of the legend image associated with the specified line name.

    Parameters:
    - parent_widget: The parent widget containing the static elements.
    - line_name (str): The line name ("bk", "mlt", "hlt") whose opacity to toggle.
    """
    # Map line names to their corresponding legend image keys
    legend_mapping = {
        "bk": "IMG_Legend_BK",
        "mlt": "IMG_Legend_MLT",
        "hlt": "IMG_Legend_HLT"
    }

    # Ensure the line name is valid
    if line_name not in legend_mapping:
        raise ValueError(f"Invalid line name: {line_name}. Must be one of {list(legend_mapping.keys())}.")

    # Get the legend image key
    legend_key = legend_mapping[line_name]

    # Check if a toggle state already exists for this line, if not, initialize it
    toggle_attr = f"{line_name}_opacity_toggled"
    if not hasattr(parent_widget, toggle_attr):
        setattr(parent_widget, toggle_attr, False)  # Initialize toggle state

    # Toggle the state
    current_state = getattr(parent_widget, toggle_attr)
    new_state = not current_state
    setattr(parent_widget, toggle_attr, new_state)

    # Set the opacity based on the toggle state
    new_opacity = 0.2 if new_state else 1.0
    set_opacity(parent_widget.static_elements[legend_key], new_opacity)

