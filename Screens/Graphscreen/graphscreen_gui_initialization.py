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
            on_normal_click=lambda: toggle_visibility_and_text(parent_widget, "bk"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_mlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_MLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: toggle_visibility_and_text(parent_widget, "mlt"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_graph_toggle_hlt_visibility': create_button(
            parent_widget=parent_widget,
            position=constants_gui.BTN_GRAPH_TOGGLE_HLT_VISIBILITY_COORDINATES,
            size=constants_gui.BTN_GRAPH_TOGGLE_VISIBILITY_SIZE,
            on_normal_click=lambda: toggle_visibility_and_text(parent_widget, "hlt"),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
    }

    # Show all buttons explicitly
    for btn in buttons.values():
        btn.show()

    return buttons

def toggle_visibility_and_text(parent_widget, line_name):
    """
    Toggle the graph line, its legend opacity, and both current & average temperature labels.
    """
    # 1) graph line
    parent_widget.temperature_graph.toggle_line_visibility(line_name)
    # 2) legend icon
    toggle_opacity(parent_widget, line_name)
    # 3) both dynamic labels
    for suffix in ("AVG_TEMP", "CUR_TEMP"):
        key = f"TXT_{suffix}_{line_name.upper()}"
        lbl = parent_widget.dynamic_elements.get(key)
        if lbl:
            lbl.setVisible(not lbl.isVisible())

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
