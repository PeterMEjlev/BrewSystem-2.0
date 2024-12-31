# graphscreen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import Common.constants as constants

class GraphScreen(QWidget):
    """
    This class represents the graph screen that opens when 'BTN_toggle_sidebar_graphs' is clicked.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.init_ui()

        layout = QVBoxLayout()

        # Placeholder content, replace with actual graphing widgets
        self.label = QLabel("Graph Screen - Add your graphs here")
        self.label.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(self.label)

        self.setLayout(layout)

    def init_ui(self):
        self.setup_window()

    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Graph Screen")
        self.showFullScreen()