import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QHBoxLayout
import Common.constants as constants
from Screens.Graphscreen.graphscreen_gui_initialization import initialize_gui_elements
from PyQt5.QtCore import Qt
from Common.TemperatureGraph import TemperatureGraph

class GraphScreen(QWidget):
    """
    This class represents the graph screen that opens when 'BTN_toggle_sidebar_graphs' is clicked.
    """
    def __init__(self):
        super().__init__()
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Assets"))
        self.init_ui()

    def init_ui(self):
        self.setup_window()
        self.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.setup_layout()  # Use a layout to position the graph and slider
        self.initialize_gui_elements()  # Initialize other GUI elements

    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Graph Screen")
        self.showFullScreen()

        from Common.config import IS_RPI
        if IS_RPI:
            self.setCursor(Qt.BlankCursor)

    def setup_layout(self):
        # Create a vertical layout for the main screen
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)  # Adjust margins if needed

        # Add the temperature graph to the layout
        self.temperature_graph = TemperatureGraph(self)
        self.layout.addWidget(self.temperature_graph)  # Add graph to layout



    def initialize_gui_elements(self):
        # Delegate GUI initialization to the external file
        initialize_gui_elements(self, self.path)

    def update_graph(self, temp_bk, temp_mlt, temp_hlt):
        """Update the graph with new temperature data."""
        if hasattr(self, 'temperature_graph'):
            self.temperature_graph.update_graph(temp_bk, temp_mlt, temp_hlt)

    def update_zoom_level(self, value):
        """
        Adjust the zoom level on the x-axis of the temperature graph based on slider value.

        Parameters:
        - value: The current value of the slider (1-100).
        """
        # Calculate zoom factor based on slider value
        zoom_factor = max(0.01, value / 100)  # Ensure zoom factor is always greater than 0

        current_range = self.temperature_graph.plot_widget.getViewBox().viewRange()[0]  # Get the current x-axis range
        center = (current_range[0] + current_range[1]) / 2  # Calculate the center of the range
        half_range = (current_range[1] - current_range[0]) / 2 * zoom_factor  # Adjust the range based on zoom factor

        new_range = [center - half_range, center + half_range]
        self.temperature_graph.plot_widget.setXRange(*new_range)

    def open_settings_screen(self):
        """
        Open the settings screen.

        This method should be connected to functionality that initializes and displays the settings screen.
        """
        from Screens.Settingsscreen.settingsscreen import SettingsScreen
        self.settings_screen = SettingsScreen()
        self.settings_screen.show()
