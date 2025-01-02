# brewscreen.py
import os
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import Qt, QThread
from Common.utils import toggle_images_visibility, apply_gradient_to_label
from Screens.Brewscreen.brewscreen_static_gui import initialize_static_elements, create_slider_plus_minus_labels
from Screens.Brewscreen.brewscreen_dynamic_gui import initialize_dynamic_elements, create_slider_value_label
import Common.constants_gui as constants_gui
import Common.constants as constants
import Common.variables as variables
from Screens.Brewscreen.brewscreen_gui_initialization import initialize_slider, initialize_buttons, hide_GUI_elements
from Common.ThermometerWorker import ThermometerWorker
from Screens.Graphscreen.graphscreen import GraphScreen
from Common.utils_rpi import change_pwm_duty_cycle
from Common.config import IS_RPI

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        self.current_selection = None  # Tracks the currently selected button
        self.active_variable = None  # Tracks the active variable being adjusted
        self.worker_thread = None  # Thread for thermometer
        self.thermometer_worker = None  # Worker instance
        self.init_ui()
        self.start_thermometer_thread()
        self.graph_screen = None  # Placeholder for the graph window        

    def init_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.initialize_gui_elements()
        self.initialize_slider_and_buttons()

    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Brewsystem 2.0")
        self.showFullScreen()
        if (IS_RPI):
            self.setCursor(Qt.BlankCursor)

    def setup_central_widget(self):
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

    def start_thermometer_thread(self):
        """Start the thermometer worker in a separate thread."""
        self.worker_thread = QThread()
        self.thermometer_worker = ThermometerWorker(self.static_elements)

        self.thermometer_worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.thermometer_worker.run)
        self.thermometer_worker.temperature_updated_bk.connect(self.update_temperature_label_bk)
        self.thermometer_worker.temperature_updated_hlt.connect(self.update_temperature_label_hlt)
        self.thermometer_worker.finished.connect(self.worker_thread.quit)
        self.thermometer_worker.finished.connect(self.thermometer_worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def stop_thermometer_thread(self):
        """Stop the thermometer worker and thread."""
        if self.thermometer_worker:
            self.thermometer_worker.stop()
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

    def update_temperature_label_bk(self, temperature):
        """Update the GUI with the new temperature."""
        # Update the temperature label dynamically
        label_key = 'TXT_TEMP_BK' 
        if label_key in self.dynamic_elements:
            if temperature >= 100:
                self.dynamic_elements[label_key].setText("100°")
            else:
                self.dynamic_elements[label_key].setText(f"{temperature:.1f}°")

    def update_temperature_label_hlt(self, temperature):
        """Update the GUI with the new temperature."""
        # Update the temperature label dynamically
        label_key = 'TXT_TEMP_HLT' 
        if label_key in self.dynamic_elements:
            if temperature >= 100:
                self.dynamic_elements[label_key].setText("100°")
            else:
                self.dynamic_elements[label_key].setText(f"{temperature:.1f}°")

    def closeEvent(self, event):
        """Ensure threads are stopped when the application is closed."""
        self.stop_thermometer_thread()
        super().closeEvent(event)

    def initialize_gui_elements(self):
        self.static_elements = initialize_static_elements(self.central_widget, self.path)
        self.dynamic_elements = initialize_dynamic_elements(self.central_widget, self.path)

        self.buttons = initialize_buttons(
        central_widget=self.central_widget,
        static_elements=self.static_elements,
        dynamic_elements=self.dynamic_elements,
        toggle_images_visibility_callback=toggle_images_visibility,
        select_button_callback=self.select_button,
        show_graph_screen_callback=self.show_graph_screen)

        hide_GUI_elements(self.static_elements, self.dynamic_elements, self.buttons)

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
        self.reset_all_gradients()

        if selected_key == 'IMG_BK_Selected' and not variables.STATE['BK_ON']:
            self.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
        elif selected_key == 'IMG_HLT_Selected' and not variables.STATE['HLT_ON']:
            self.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()

    def select_new_button(self, selected_key, name_key):
        # If the same label is already active, deselect it and reset colors
        if self.current_selection == selected_key:
            self.current_selection = None
            self.reset_all_gradients()
            self.hide_slider_elements()
            return

        # Reset gradients for all labels
        self.reset_all_gradients()

        # Apply gradient only to the selected label
        apply_gradient_to_label(self, selected_key)

        # Update the current selection
        self.current_selection = selected_key
        self.show_slider_elements()

        if selected_key == 'IMG_BK_Selected':
            self.dynamic_elements['TXT_EFFICIENCY_BK'].show()
            if not variables.STATE['HLT_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()

        elif selected_key == 'IMG_HLT_Selected':
            self.dynamic_elements['TXT_EFFICIENCY_HLT'].show()
            if not variables.STATE['BK_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
        
        else:
            self.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
            self.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()    
   
    def reset_all_gradients(self):
        """
        Reset gradients for all labels to their default state (white).
        """
        labels_to_reset = [
            'TXT_EFFICIENCY_BK',
            'TXT_EFFICIENCY_HLT',
            'TXT_TEMP_REG_BK',
            'TXT_TEMP_REG_HLT',
            'TXT_PUMP_SPEED_P1',
            'TXT_PUMP_SPEED_P2'
        ]
        for label_key in labels_to_reset:
            self.dynamic_elements[label_key].gradient_colors = None
            self.dynamic_elements[label_key].update()

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

        # Hide the slider set buttons
        if 'BTN_set_slider_0' in self.buttons and 'BTN_set_slider_100' in self.buttons:
            self.buttons['BTN_set_slider_0'].hide()
            self.buttons['BTN_set_slider_100'].hide()

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

        # Show the slider set buttons
        if 'BTN_set_slider_0' in self.buttons and 'BTN_set_slider_100' in self.buttons:
            self.buttons['BTN_set_slider_0'].show()
            self.buttons['BTN_set_slider_100'].show()
        
    def on_slider_change(self, value):
        self.slider_value_label.setText(str(value))
        self.adjust_fake_slider_width(value)
        self.update_active_variable(value)

    def adjust_fake_slider_width(self, value):
        max_width = constants_gui.SLIDER_SIZE[0]
        new_width = int((value / self.slider.maximum()) * max_width)
        self.fake_slider.setGeometry(
            self.fake_slider.geometry().x(),
            self.fake_slider.geometry().y(),
            new_width,
            self.fake_slider.geometry().height()
        )

    def update_active_variable(self, value):
        if self.active_variable:
            print(f"Updating {self.active_variable} to {value}")
            setattr(variables, self.active_variable, value)
            label_key = f'TXT_{self.active_variable.upper()}'

            # Determine the appropriate suffix based on the variable type
            if 'PUMP_SPEED' in self.active_variable.upper() or 'EFFICIENCY' in self.active_variable.upper():
                suffix = '%'  # Percentage for pump speed
            else:
                suffix = '°'  # Degree for temperature

            if label_key in self.dynamic_elements:
                self.dynamic_elements[label_key].setText(f"{value}{suffix}")
            else:
                print(f"Label key {label_key} not found in dynamic elements.")

            # Update the REG values specifically if the active variable is temp_REG_BK or temp_REG_HLT
            if self.active_variable == 'temp_REG_BK':
                variables.temp_REG_BK = value
            elif self.active_variable == 'temp_REG_HLT':
                variables.temp_REG_HLT = value

            # Update the PWM duty cycle if the active variable is a PWM signal
            if self.active_variable == 'efficiency_BK':
                change_pwm_duty_cycle(variables.BK_PWM, value)
            elif self.active_variable == 'efficiency_HLT':
                change_pwm_duty_cycle(variables.HLT_PWM, value)

    def update_slider_value(self, variable_name):
        variables.active_variable = variable_name  # Store the active variable globally
        self.active_variable = variable_name  # Update the local reference

        value = getattr(variables, variable_name, None)
        if value is not None:
            self.slider.setValue(value)
            self.slider_value_label.setText(str(value))

    def set_slider_value(self, value):
        """
        Sets the slider to a specified value and updates the active variable.
        """
        if self.active_variable is not None:
            self.slider.setValue(value)  # Set the slider value
            self.update_active_variable(value)  # Update the active variable and UI

    def mousePressEvent(self, event):
        """
        Handle mouse press events to deselect button when clicking outside of a button.
        """
        # Check if the click was inside any button's geometry
        clicked_on_button = any(
            button.geometry().contains(event.pos()) for button in self.buttons.values()
        )

        if not clicked_on_button and self.current_selection is not None:
            # If click is outside buttons and a button is currently selected, reset colors and deselect
            self.reset_all_gradients()
            self.current_selection = None
            self.hide_slider_elements()

            if not variables.STATE['BK_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
            if not variables.STATE['HLT_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()

        # Call the base class method to ensure other events are handled
        super().mousePressEvent(event)

    def show_graph_screen(self):
        if not self.graph_screen:
            self.graph_screen = GraphScreen()
        self.graph_screen.show()
