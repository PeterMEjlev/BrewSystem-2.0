import os
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import Qt
from Common.utils import create_slider, create_label, create_image, create_button, toggle_images_visibility
from Screens.static_gui import initialize_static_elements  # Import the static elements initializer
import Common.constants as constants


class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define the base path for relative asset loading
        self.path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        self.current_selection = None  # Tracks the currently selected button
        self.init_ui()

    def init_ui(self):
        # Configure window properties
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Brewsystem 2.0")
        self.showFullScreen()

        # Central widget without margins
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.central_widget.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.setCentralWidget(self.central_widget)

        # Initialize static GUI elements
        self.static_elements = initialize_static_elements(self.central_widget, self.path)
        
        # Hide necessary GUI elements
        self.hide_GUI_elements()
        
        # Initialize slider
        self.initialize_slider()
        
        # Initialize buttons
        self.initialize_buttons()

    def hide_GUI_elements(self):
        """
        Hides specific static images initialized in the static GUI.
        """
        # Pot on gradients
        self.static_elements['IMG_Pot_BK_On_Background'].hide()
        self.static_elements['IMG_Pot_BK_On_Foreground'].hide()
        self.static_elements['IMG_Pot_MLT_On_Background'].hide()
        self.static_elements['IMG_Pot_MLT_On_Foreground'].hide()
        self.static_elements['IMG_Pot_HLT_On_Background'].hide()
        self.static_elements['IMG_Pot_HLT_On_Foreground'].hide()
        
        # Selection Boxes
        self.static_elements['IMG_BK_Selected'].hide()
        self.static_elements['IMG_HLT_Selected'].hide()
        self.static_elements['IMG_P1_Selected'].hide()
        self.static_elements['IMG_P2_Selected'].hide()

        # Pot and Pump Names
        self.static_elements['TXT_POT_NAME_BK'].show()
        self.static_elements['TXT_POT_NAME_MLT'].show()
        self.static_elements['TXT_POT_NAME_HLT'].show()
        self.static_elements['TXT_P1'].show()
        self.static_elements['TXT_P2'].show()

    def initialize_slider(self):
        """
        Initializes the slider and its value label.
        """
        # Add slider to the screen
        self.slider = create_slider(
            parent_widget=self.central_widget,
            orientation=Qt.Horizontal,
            minimum=constants.SLIDER_MIN,
            maximum=constants.SLIDER_MAX,
            value=50,
            location=constants.SLIDER_COORDINATES,
            size=constants.SLIDER_SIZE
        )
        # Connect slider change to a function
        self.slider.valueChanged.connect(self.on_slider_change)

        # Add a label to display the slider value
        self.value_label = create_label(
            parent_widget=self.central_widget,
            text=str(self.slider.value()),
            color='white',
            size=constants.TXT_SLIDER_VALUE_SIZE,
            location=(constants.TXT_SLIDER_VALUE_COORDINATES)
        )

    def initialize_buttons(self):
        """
        Initializes the buttons used in the GUI.
        """
        self.BTN_toggle_BK = create_button(
            parent_widget=self.central_widget,
            position=constants.IMG_POT_BK_COORDINATES,
            size=constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: self.select_button('IMG_BK_Selected', 'TXT_POT_NAME_BK'),
            on_long_click=lambda: toggle_images_visibility(self.static_elements, ['IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground']),
            invisible=True
        )
        self.BTN_toggle_HLT = create_button(
            parent_widget=self.central_widget,
            position=constants.IMG_POT_HLT_COORDINATES,
            size=constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: self.select_button('IMG_HLT_Selected', 'TXT_POT_NAME_HLT'),
            on_long_click=lambda: toggle_images_visibility(self.static_elements, ['IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground']),
            invisible=True
        )
        self.BTN_toggle_P1 = create_button(
            parent_widget=self.central_widget,
            position=constants.IMG_PUMP_BOX_P1_COORDINATES,
            size=constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: self.select_button('IMG_P1_Selected', 'TXT_P1'),
            on_long_click=None,
            invisible=True
        )
        self.BTN_toggle_P2 = create_button(
            parent_widget=self.central_widget,
            position=constants.IMG_PUMP_BOX_P2_COORDINATES,
            size=constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: self.select_button('IMG_P2_Selected', 'TXT_P2'),
            on_long_click=None,
            invisible=True
        )

    def select_button(self, selected_key, name_key):
        """
        Ensures only one selection box is visible at a time and updates the current selection.
        
        Parameters:
        selected_key (str): The key of the image to show or hide.
        name_key (str): The key of the name text to hide or show.
        """
        # If the selected button is already selected, unselect it
        if self.current_selection == selected_key:
            if selected_key in self.static_elements:
                self.static_elements[selected_key].hide()  # Hide the current selection
            if name_key in self.static_elements:
                self.static_elements[name_key].show()  # Show the name text
            self.current_selection = None  # Reset the current selection
        else:
            # Hide all selection boxes
            selection_keys = ['IMG_BK_Selected', 'IMG_HLT_Selected', 'IMG_P1_Selected', 'IMG_P2_Selected']
            name_keys = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2']
            for key in selection_keys:
                if key in self.static_elements:
                    self.static_elements[key].hide()
            for key in name_keys:
                if key in self.static_elements:
                    self.static_elements[key].show()
            
            # Show the new selected selection box
            if selected_key in self.static_elements:
                self.static_elements[selected_key].show()
            if name_key in self.static_elements:
                self.static_elements[name_key].hide()
            self.current_selection = selected_key  # Update current selection

    def on_slider_change(self, value):
        """
        Updates the slider value label when the slider is moved.
        """
        self.value_label.setText(str(value))  # Update the label text
