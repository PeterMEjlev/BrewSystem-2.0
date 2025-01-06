import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
        self.setup_layout()
        self.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.initialize_gui_elements()

    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Graph Screen")
        self.showFullScreen()
        #self.hide()

        from Common.config import IS_RPI
        if (IS_RPI):
            self.setCursor(Qt.BlankCursor)

    def setup_layout(self):
        # Set up a layout for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add the temperature graph to the layout
        self.temperature_graph = TemperatureGraph(self)
        self.layout.addWidget(self.temperature_graph)

    def initialize_gui_elements(self):
        # Delegate GUI initialization to the external file
        initialize_gui_elements(self, self.path)

    def open_settings_screen(self):
        from Screens.Settingsscreen.settingsscreen import SettingsScreen
        self.settings_screen = SettingsScreen()  # Instantiate the GraphScreen
        self.settings_screen.show()  # Show the graph screen

    def update_graph(self, temp_bk, temp_mlt, temp_hlt):
        """Update the graph with new temperature data."""
        if hasattr(self, 'temperature_graph'):
            self.temperature_graph.update_graph(temp_bk, temp_mlt, temp_hlt)