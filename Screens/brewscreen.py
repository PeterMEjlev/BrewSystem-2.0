# brewscreen.py
import os
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import Qt
from Common.utils import toggle_images_visibility
from Screens.static_gui import initialize_static_elements, create_slider_plus_minus_labels
from Screens.dynamic_gui import initialize_dynamic_elements, create_slider_value_label
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
        self.setup_window()
        self.setup_central_widget()
        self.initialize_gui_elements()
        self.initialize_slider_and_buttons()


    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Brewsystem 2.0")
        self.showFullScreen()

    def setup_central_widget(self):
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

    def initialize_gui_elements(self):
        self.static_elements = initialize_static_elements(self.central_widget, self.path)
        self.dynamic_elements = initialize_dynamic_elements(self.central_widget, self.path)
        hide_GUI_elements(self.static_elements)

    def initialize_slider_and_buttons(self):
        """
        Initialize the slider and buttons for the GUI.
        """
        # Initialize the slider and its related elements
        self.slider, _, self.fake_slider, self.fake_slider_background = initialize_slider(
            central_widget=self.central_widget,
            constants=constants,
            on_slider_change_callback=self.on_slider_change,
            dynamic_elements=self.dynamic_elements
        )

        # Create the slider value label and set it to self.value_label
        self.slider_value_label = create_slider_value_label(self.central_widget)
        self.dynamic_elements['TXT_SLIDER_VALUE'] = self.slider_value_label

        # Create the plus/minus slider labels and store them in self.slider_plus_minus_labels
        self.slider_plus_minus_labels = create_slider_plus_minus_labels(self.central_widget)
        self.dynamic_elements.update(self.slider_plus_minus_labels)

        
        for label in self.slider_plus_minus_labels.values():
            label.hide()

        # Initialize the buttons
        self.buttons = initialize_buttons(
            central_widget=self.central_widget,
            constants=constants,
            static_elements=self.static_elements,
            toggle_images_visibility_callback=toggle_images_visibility,
            select_button_callback=self.select_button
        )

    def select_button(self, selected_key, name_key):
        if self.current_selection == selected_key:
            self.deselect_button(selected_key, name_key)
        else:
            self.select_new_button(selected_key, name_key)

    def deselect_button(self, selected_key, name_key):
        self.hide_element(selected_key)
        self.show_element(name_key)
        self.current_selection = None
        self.hide_slider_elements()

    def select_new_button(self, selected_key, name_key):
        self.hide_all_selection_boxes()
        self.show_element(selected_key)
        self.hide_element(name_key)
        self.current_selection = selected_key
        self.show_slider_elements()

    def hide_all_selection_boxes(self):
        selection_keys = ['IMG_BK_Selected', 'IMG_HLT_Selected', 'IMG_P1_Selected', 'IMG_P2_Selected', 'IMG_REGBK_Selected', 'IMG_REGHLT_Selected']
        name_keys = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2', 'TXT_REG_BK', 'TXT_REG_HLT']
        for key in selection_keys:
            self.hide_element(key)
        for key in name_keys:
            self.show_element(key)

    def hide_element(self, key):
        if key in self.static_elements:
            self.static_elements[key].hide()

    def show_element(self, key):
        if key in self.static_elements:
            self.static_elements[key].show()

    def hide_slider_elements(self):
        self.slider.hide()
        self.fake_slider.hide()
        self.fake_slider_background.hide()
        self.slider_value_label.hide()
        self.static_elements['TXT_Slider_0'].hide()
        self.static_elements['TXT_Slider_100'].hide()

        # Hide plus minus labels for slider
        for label in self.slider_plus_minus_labels.values():
            label.hide()

    def show_slider_elements(self):
        self.slider.show()
        self.fake_slider.show()
        self.fake_slider_background.show()
        self.slider_value_label.show()
        self.static_elements['TXT_Slider_0'].show()
        self.static_elements['TXT_Slider_100'].show()

        # Show plus minus labels for slider
        for label in self.slider_plus_minus_labels.values():
            label.show()
        
    def on_slider_change(self, value):
        self.slider_value_label.setText(str(value))
        self.adjust_fake_slider_width(value)
        self.update_active_variable(value)

    def adjust_fake_slider_width(self, value):
        max_width = constants.SLIDER_SIZE[0]
        new_width = int((value / self.slider.maximum()) * max_width)
        self.fake_slider.setGeometry(
            self.fake_slider.geometry().x(),
            self.fake_slider.geometry().y(),
            new_width,
            self.fake_slider.geometry().height()
        )

    def update_active_variable(self, value):
        if self.active_variable:
            setattr(variables, self.active_variable, value)
            label_key = f'TXT_{self.active_variable.upper()}'

            # Determine the appropriate suffix based on the variable type
            if 'PUMP_SPEED' in self.active_variable.upper():
                suffix = '%'  # Percentage for pump speed
            else:
                suffix = '°'  # Degree for temperature

            if label_key in self.dynamic_elements:
                self.dynamic_elements[label_key].setText(f"{value}{suffix}")
            else:
                print(f"Label key {label_key} not found in dynamic elements.")

            print(self.active_variable)

    def update_slider_value(self, variable_name):
        variables.active_variable = variable_name  # Store the active variable globally
        self.active_variable = variable_name  # Update the local reference

        value = getattr(variables, variable_name, None)
        if value is not None:
            self.slider.setValue(value)
            self.slider_value_label.setText(str(value))

