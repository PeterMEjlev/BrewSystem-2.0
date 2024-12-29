# brewscreen.py
import os
from PyQt5.QtWidgets import QMainWindow, QWidget
from Common.utils import toggle_images_visibility
from Screens.static_gui import initialize_static_elements  # Import the static elements initializer
from Screens.dynamic_gui import initialize_dynamic_elements  # Import the dynamic elements initializer
import Common.constants as constants
import Common.variables as variables
from gui_initialization import initialize_slider, initialize_buttons, hide_GUI_elements

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        self.current_selection = None  # Tracks the currently selected button
        self.active_variable = None  # Tracks the active variable being adjusted
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

        # Initialize static & dynamic GUI elements
        self.static_elements = initialize_static_elements(self.central_widget, self.path)
        self.dynamic_elements = initialize_dynamic_elements(self.central_widget, self.path)

        # Hide necessary GUI elements
        hide_GUI_elements(self.static_elements)

        # Initialize slider
        self.slider, self.value_label = initialize_slider(
            central_widget=self.central_widget,
            constants=constants,
            on_slider_change_callback=self.on_slider_change
        )

        # Initialize buttons (last to ensure they are on top)
        self.buttons = initialize_buttons(
            central_widget=self.central_widget,
            constants=constants,
            static_elements=self.static_elements,
            toggle_images_visibility_callback=toggle_images_visibility,
            select_button_callback=self.select_button
        )

    def select_button(self, selected_key, name_key):
        """
        Ensures only one selection box is visible at a time and updates the current selection.
        Also shows the slider if a selection is active.

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
            self.slider.hide()  # Hide slider
            self.value_label.hide()  # Hide label
            self.static_elements['TXT_Slider_0'].hide()  # Hide slider labels
            self.static_elements['TXT_Slider_100'].hide()  # Hide slider labels
        else:
            # Hide all selection boxes
            selection_keys = ['IMG_BK_Selected', 'IMG_HLT_Selected', 'IMG_P1_Selected', 'IMG_P2_Selected',
                              'IMG_REGBK_Selected', 'IMG_REGHLT_Selected']
            name_keys = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2', 'TXT_REG_BK', 'TXT_REG_HLT']
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
            self.slider.show()  # Show slider
            self.value_label.show()  # Show label
            self.static_elements['TXT_Slider_0'].show()  # Show slider labels
            self.static_elements['TXT_Slider_100'].show()  # Show slider labels

    def on_slider_change(self, value):
        """
        Updates the slider value label and the respective variable and label when the slider is moved.
        """
        self.value_label.setText(str(value))  # Update the slider label

        # Update the value of the active variable in variables.py
        if self.active_variable:
            setattr(variables, self.active_variable, value)

            # Update the respective label in dynamic_elements
            label_key = f'TXT_{self.active_variable.upper()}'
            if label_key in self.dynamic_elements:
                self.dynamic_elements[label_key].setText(f"{value}°")
            else:
                print(f"Label key {label_key} not found in dynamic elements.")


    def update_slider_value(self, variable_name):
        """
        Updates the slider value based on the selected variable and sets the active variable.

        Parameters:
        - variable_name (str): The name of the variable from `variables.py` whose value should set the slider.
        """
        self.active_variable = variable_name  # Set the active variable
        value = getattr(variables, variable_name, None)
        if value is not None:
            self.slider.setValue(value)  # Update the slider value
            self.value_label.setText(str(value))  # Update the slider label

