# brewscreen.py
import os, math, time
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import Qt, QThread
from Common.utils import toggle_images_visibility, play_audio
from Screens.Brewscreen.brewscreen_static_gui import initialize_static_elements, create_slider_plus_minus_labels
from Screens.Brewscreen.brewscreen_dynamic_gui import initialize_dynamic_elements, create_slider_value_label
import Common.constants_gui as constants_gui
import Common.constants as constants
import Common.variables as variables
from Screens.Brewscreen.brewscreen_gui_initialization import initialize_slider, initialize_buttons, hide_GUI_elements
from Common.ThermometerWorker import ThermometerWorker
from Common.TemperatureGraph import TemperatureGraph
from Screens.Graphscreen.graphscreen import GraphScreen
from Screens.Settingsscreen.settingsscreen import SettingsScreen
from Common.utils_rpi import change_pwm_duty_cycle, initialize_gpio
import Screens.Brewscreen.brewscreen_helpers as brewscreen_helpers
import Screens.Brewscreen.brewscreen_events as brewscreen_events
from Common.gif_viewer import GifViewer
from Common.detector_signals import detector_signals
from Common.bruce_gifs import start_gif, stop_gif
from Common.max_wattage import calculate_new_total_power_consumption, power_is_within_limit, calculate_max_new_efficiency

gif_label_thinking = None
gif_label_responding = None
gif_label_listening = None

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        initialize_gpio()
        self.current_selection = None  # Tracks the currently selected button
        self.active_variable = None  # Tracks the active variable being adjusted
        self.worker_thread = None  # Thread for thermometer
        self.thermometer_worker = None  # Worker instance
        self.graph = TemperatureGraph(self)

        self.init_ui()  # Call setup functions first to initialize central_widget
        
        # Initialize the graph screen
        self.graph_screen = GraphScreen()
        self.graph_screen.hide()
        self.graph = self.graph_screen.temperature_graph  # Reference the temperature graph from GraphScreen

        self.settings_screen = None  # Placeholder for the settings window    

        self.start_thermometer_thread() 

        self.last_audio_play_time = 0  # Store last time audio played
        self.audio_cooldown = 1  # Cooldown in seconds

    def init_ui(self):
        self.setup_window()
        self.setup_central_widget()
        self.initialize_gui_elements()
        self.initialize_slider_and_buttons()

        self.gif_label_loading = self.initialize_bruce_loading_gif_label(self.central_widget)
        self.gif_label_responding = self.initialize_bruce_responding_gif_label(self.central_widget)
        self.gif_label_listening = self.initialize_bruce_listening_gif_label(self.central_widget)

        detector_signals.bruce_quitting.connect(
            lambda: (
                stop_gif(self.gif_label_loading),
                stop_gif(self.gif_label_responding),
                stop_gif(self.gif_label_listening)
            )
        )

    def setup_window(self):
        self.setGeometry(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.setWindowTitle("Brewsystem 2.0")
        self.showFullScreen()

        from Common.config import IS_RPI
        if IS_RPI:
            self.setCursor(Qt.BlankCursor)

    def setup_central_widget(self):
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"background-color: {constants.BACKGROUND_COLOR};")
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

    def start_thermometer_thread(self):
        """Start the thermometer worker in a separate thread."""
        self.worker_thread = QThread()
        self.thermometer_worker = ThermometerWorker(self.static_elements, self.graph_screen.temperature_graph)

        self.thermometer_worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.thermometer_worker.run)
        self.thermometer_worker.temperature_updated_bk.connect(self.update_temperature_label_bk)
        self.thermometer_worker.temperature_updated_mlt.connect(self.update_temperature_label_mlt)
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

    def update_temperature_label_mlt(self, temperature):
        """Update the GUI with the new temperature."""
        # Update the temperature label dynamically
        label_key = 'TXT_TEMP_MLT' 
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

    def initialize_bruce_loading_gif_label(self, parent_widget):
        gif_label = GifViewer(parent_widget, "bruce_loading.gif", constants_gui.IMG_VOICELINES[0], constants_gui.IMG_VOICELINES[1], 129, 97)
        gif_label.show()
        self.gif_label_loading = gif_label
        detector_signals.bruce_loading.connect(
            lambda: (
                start_gif(self.gif_label_loading),
                stop_gif(self.gif_label_responding),
                stop_gif(self.gif_label_listening)
            )
        )
        return gif_label
    
    def initialize_bruce_responding_gif_label(self, parent_widget):
        gif_label = GifViewer(parent_widget, "bruce_responding.gif", constants_gui.IMG_VOICELINES[0], constants_gui.IMG_VOICELINES[1], 129, 97)
        gif_label.show()
        self.gif_label_responding = gif_label
        detector_signals.bruce_responding.connect(
            lambda: (
                stop_gif(self.gif_label_loading),
                start_gif(self.gif_label_responding),
                stop_gif(self.gif_label_listening)
            )
        )
        return gif_label
    
    def initialize_bruce_listening_gif_label(self, parent_widget):
        gif_label = GifViewer(parent_widget, "bruce_listening.gif", constants_gui.IMG_VOICELINES[0], constants_gui.IMG_VOICELINES[1], 129, 97)
        gif_label.show()
        self.gif_label_listening = gif_label
        detector_signals.bruce_listening.connect(
            lambda: (
                stop_gif(self.gif_label_loading),
                stop_gif(self.gif_label_responding),
                start_gif(self.gif_label_listening)
            )
        )
        return gif_label     

    def initialize_gui_elements(self):
        self.static_elements = initialize_static_elements(self.central_widget, self.path)
        self.dynamic_elements = initialize_dynamic_elements(self.central_widget, self.path)

        self.buttons = initialize_buttons(
        central_widget=self.central_widget,
        static_elements=self.static_elements,
        dynamic_elements=self.dynamic_elements,
        toggle_images_visibility_callback=toggle_images_visibility,
        select_button_callback=brewscreen_events.select_button,
        show_graph_screen_callback=self.show_graph_screen,
        show_settings_screen_callback=self.show_settings_screen,
        instance=self
        )

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

    def reset_current_selection(self) -> None:
        """Reset the current selection and hide slider elements."""
        self.current_selection = None
        self.reset_all_gradients_and_colour()
        self.hide_slider_elements()

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
        """
        Handles changes in the slider value and prevents updates if efficiency values exceed the power limit.
        """
        if self.active_variable in ['efficiency_BK', 'efficiency_HLT']:
            # Check power limit before updating slider and variable
            if not power_is_within_limit(calculate_new_total_power_consumption(self.active_variable, value)):
                self.slider.setValue(getattr(variables, self.active_variable))  # Revert to the last valid value
                
                # Cooldown check: Prevent multiple audio triggers
                current_time = time.time()
                if current_time - self.last_audio_play_time >= self.audio_cooldown:
                    play_audio("max_power_consumption - Male.mp3")
                    self.last_audio_play_time = current_time  # Update last played time

                return

        # Update UI elements
        self.slider_value_label.setText(str(value))
        self.update_active_variable(value)

    def update_active_variable(self, value):
        if self.active_variable:
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
            elif self.active_variable == 'efficiency_BK':
                if power_is_within_limit(calculate_new_total_power_consumption('efficiency_BK',value)):
                    change_pwm_duty_cycle(variables.BK_PWM, value)
            elif self.active_variable == 'efficiency_HLT':
                if power_is_within_limit(calculate_new_total_power_consumption('efficiency_HLT',value)):
                    change_pwm_duty_cycle(variables.HLT_PWM, value)
            elif self.active_variable == 'pump_speed_P1':
                change_pwm_duty_cycle(variables.P1_PWM, value)
            elif self.active_variable == 'pump_speed_P2':
                change_pwm_duty_cycle(variables.P2_PWM, value)

    def update_slider_value(self, variable_name):
        self.active_variable = variable_name  # Update the local reference

        value = getattr(variables, variable_name, None)
        if value is not None:
            self.slider.setValue(value)
            self.slider_value_label.setText(str(value))

    def set_slider_value(self, value):
        """
        Sets the slider to a specified value and updates the active variable
        only if the power is within the limit.
        """
        if self.active_variable in ['efficiency_BK', 'efficiency_HLT']:
            # Check if the new value is within the power limit
            if not power_is_within_limit(calculate_new_total_power_consumption(self.active_variable, value)):
                value = math.floor(calculate_max_new_efficiency(self.active_variable))
                play_audio("max_power_consumption - Male.mp3")

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
            brewscreen_helpers.reset_all_gradients_and_colour(self)
            self.current_selection = None
            self.hide_slider_elements()

            if not variables.STATE['BK_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
            if not variables.STATE['HLT_ON']:
                self.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()

        self.reset_active_variable()

        # Call the base class method to ensure other events are handled
        super().mousePressEvent(event)

    def show_graph_screen(self):
        if not self.graph_screen:
            self.graph_screen = GraphScreen()
        self.graph_screen.show()

    def show_settings_screen(self):
        if not self.settings_screen:
            self.settings_screen = SettingsScreen()
        self.settings_screen.show()

    def update_active_variable_for_selection(self, selected_key):
        """
        Update the active variable based on the selected button key.

        Parameters:
        - selected_key (str): The key of the selected button.

        Returns:
        None
        """
        # Map of selected keys to corresponding active variables
        key_to_variable_map = {
            'IMG_BK_Selected': 'efficiency_BK',
            'IMG_HLT_Selected': 'efficiency_HLT',
            'IMG_P1_Selected': 'pump_speed_P1',
            'IMG_P2_Selected': 'pump_speed_P2',
            'IMG_REGBK_Selected': 'temp_REG_BK',
            'IMG_REGHLT_Selected': 'temp_REG_HLT'
        }

        # Update active_variable based on the map, default to None if key is not found
        self.active_variable = key_to_variable_map.get(selected_key)
        variables.active_variable = self.active_variable  # Update global active_variable

    def reset_active_variable(self):
        self.active_variable = None
        variables.active_variable = None
