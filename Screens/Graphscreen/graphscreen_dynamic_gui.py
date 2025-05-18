from Common.utils import create_label
import Common.variables as variables
import Common.constants_gui as constants_gui
from PyQt5.QtCore import Qt


def initialize_dynamic_text(parent_widget):
    """
    Initialize dynamic text on the GraphScreen.
    """
    # Width set to accommodate full temperature text without cropping
    label_width = getattr(constants_gui, 'TXT_GRAPH_TEMP_TEXT_WIDTH', 200)

    return {
        # Current pot temperatures displayed on the graph screen
        'TXT_CUR_TEMP_BK': create_label(
            parent_widget,
            f"BK: {variables.temp_BK:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_TEMP_BK_GRAPH_COORDINATES,
            width=label_width,
            alignment=Qt.AlignCenter
        ),
        'TXT_CUR_TEMP_MLT': create_label(
            parent_widget,
            f"MLT: {variables.temp_MLT:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_TEMP_MLT_GRAPH_COORDINATES,
            width=label_width,
            alignment=Qt.AlignCenter
        ),
        'TXT_CUR_TEMP_HLT': create_label(
            parent_widget,
            f"HLT: {variables.temp_HLT:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_TEMP_HLT_GRAPH_COORDINATES,
            width=label_width,
            alignment=Qt.AlignCenter
        ),
        # Average pot temperatures (initially zero, updated elsewhere)
        'TXT_AVG_TEMP_BK': create_label(
            parent_widget,
            f"{variables.average_temp_time_window} min: {0.0:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_AVG_TEMP_BK_GRAPH_COORDINATES,
            width=label_width+50,
            alignment=Qt.AlignCenter
        ),
        'TXT_AVG_TEMP_MLT': create_label(
            parent_widget,
            f"{variables.average_temp_time_window} min: {0.0:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_AVG_TEMP_MLT_GRAPH_COORDINATES,
            width=label_width+50,
            alignment=Qt.AlignCenter
        ),
        'TXT_AVG_TEMP_HLT': create_label(
            parent_widget,
            f"{variables.average_temp_time_window} min: {0.0:.1f}°C",
            color='white',
            size=constants_gui.TXT_GRAPH_TEMP_SIZE,
            center=constants_gui.TXT_AVG_TEMP_HLT_GRAPH_COORDINATES,
            width=label_width+50,
            alignment=Qt.AlignCenter
        ),
    }


def initialize_dynamic_elements(parent_widget, assets_path):
    """
    Initialize all dynamic GUI text elements for the GraphScreen.

    Returns:
        dict: A dictionary of dynamic QLabel references.
    """
    dynamic_text = initialize_dynamic_text(parent_widget)
    return {**dynamic_text}
