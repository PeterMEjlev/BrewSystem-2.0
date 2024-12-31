import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import Common.constants as constants
from Screens.Graphscreen.graphscreen_gui_initialization import initialize_gui_elements


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

    def setup_layout(self):
        # Set up a layout for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def initialize_gui_elements(self):
        # Delegate GUI initialization to the external file
        initialize_gui_elements(self, self.path)
