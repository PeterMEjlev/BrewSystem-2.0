# brewscreen_gui_initialization.py
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
import Common.constants
from Common.utils import create_slider, create_button, toggle_variable, set_variable, set_label_text_color, set_images_visibility, play_audio
from Common.utils_rpi import set_pwm_signal, stop_pwm_signal, create_software_pwm
from Common.variables import STATE
from Common.constants import SLIDER_PAGESTEP
import Common.constants_rpi as constants_rpi
import Common.constants_gui as constants_gui
import Common.variables as variables
from Common.shutdown import perform_shutdown
from Common.max_wattage import calculate_new_total_power_consumption, power_is_within_limit

_gui_static_elements = None
_gui_dynamic_elements = None
_gui_toggle_images_visibility_callback = None

def initialize_slider(central_widget, constants, on_slider_change_callback, dynamic_elements):
    # Create the real slider
    slider = create_slider(
        parent_widget=central_widget,
        orientation=Qt.Horizontal,
        minimum=constants.SLIDER_MIN,
        maximum=constants.SLIDER_MAX,
        value=50,
        location=constants_gui.SLIDER_COORDINATES,
        size=constants_gui.SLIDER_SIZE
    )
    slider.setPageStep(SLIDER_PAGESTEP)
    slider.hide()
    slider.valueChanged.connect(on_slider_change_callback)

    # Store the last valid value on the slider
    slider.last_valid_value = slider.value()

    # Create background for the fake slider
    fake_slider_background = QtWidgets.QFrame(central_widget)
    fake_slider_background.setGeometry(
        constants_gui.SLIDER_COORDINATES[0],
        constants_gui.SLIDER_COORDINATES[1] + 15,
        int(constants_gui.SLIDER_SIZE[0]),
        constants_gui.SLIDER_SIZE[1] + 10
    )
    fake_slider_background.setStyleSheet("""
        background-color: #292728;
        border-radius: 20px;
    """)
    fake_slider_background.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    fake_slider_background.hide()

    # Create the fake slider
    fake_slider = QtWidgets.QFrame(central_widget)
    fake_slider.setGeometry(
        constants_gui.SLIDER_COORDINATES[0],
        constants_gui.SLIDER_COORDINATES[1] + 15,
        int(constants_gui.SLIDER_SIZE[0] * 0.5),
        constants_gui.SLIDER_SIZE[1] + 10
    )

    def update_border_radius(value):
        # Check if we're updating an efficiency value and if the new power is allowed
        if variables.active_variable in ['efficiency_BK', 'efficiency_HLT']:
            new_total_power = calculate_new_total_power_consumption(variables.active_variable, value)
            if not power_is_within_limit(new_total_power):
                # Revert to the last valid value if the limit would be exceeded.
                slider.blockSignals(True)
                slider.setValue(slider.last_valid_value)
                slider.blockSignals(False)
                return
        # Otherwise, update last_valid_value to this acceptable value
        slider.last_valid_value = value

        # Proceed with updating the fake slider
        max_width = constants_gui.SLIDER_SIZE[0]
        new_width = int((value / slider.maximum()) * max_width)
        border_radius = min(new_width // 2, 20)
        fake_slider.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #F04C65, stop:1 #F58361);
            border-radius: {border_radius}px;
        """)
        fake_slider.setGeometry(
            fake_slider.geometry().x(),
            fake_slider.geometry().y(),
            new_width,
            fake_slider.geometry().height()
        )

    # Connect the valueChanged signal to update the fake slider
    slider.valueChanged.connect(update_border_radius)

    fake_slider.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    fake_slider.hide()

    value_label = dynamic_elements.get('TXT_SLIDER_VALUE', None)

    return slider, value_label, fake_slider, fake_slider_background

def initialize_buttons(central_widget, static_elements, dynamic_elements, toggle_images_visibility_callback, select_button_callback, show_graph_screen_callback, show_settings_screen_callback, instance):
    """
    Initializes the buttons used in the GUI.

    Parameters:
    - central_widget: The parent widget for the buttons.
    - constants: Constants containing button properties.
    - static_elements: Dictionary of static elements for the GUI.
    - toggle_images_visibility_callback: Function to toggle visibility of images.
    - select_button_callback: Function to handle button selection logic.

    Returns:
    A dictionary of initialized buttons.
    """
    # Set our global references for pot toggling here, once.
    set_pot_toggle_references(
        static_elements, 
        dynamic_elements, 
        toggle_images_visibility_callback
    )
    
    buttons = {
        'BTN_toggle_BK': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_POT_BK_COORDINATES,
            size=constants_gui.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_BK_Selected', 'TXT_EFFICIENCY_BK'),  # Pass self explicitly
                central_widget.parent().update_slider_value('efficiency_BK')  # Update slider for BK
            ),
            on_long_click=lambda: toggle_pot_handle_all('BK'),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_HLT': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_POT_HLT_COORDINATES,
            size=constants_gui.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_HLT_Selected', 'TXT_EFFICIENCY_HLT'),
                central_widget.parent().update_slider_value('efficiency_HLT')  # Update slider for HLT
            ),
            on_long_click=lambda: toggle_pot_handle_all('HLT'),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_P1': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_PUMP_BOX_P1_COORDINATES,
            size=constants_gui.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_P1_Selected', 'TXT_P1'),
                central_widget.parent().update_slider_value('pump_speed_P1')  # Update slider for P1
            ),
            on_long_click=lambda: toggle_pump_handle_all('P1'),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_P2': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_PUMP_BOX_P2_COORDINATES,
            size=constants_gui.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_P2_Selected', 'TXT_P2'),
                central_widget.parent().update_slider_value('pump_speed_P2')  # Update slider for P2
            ),
            on_long_click=lambda: toggle_pump_handle_all('P2'),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_REGBK': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_REG_ON_OFF_BK_COORDINATES,
            size=constants_gui.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_REGBK_Selected', 'TXT_REG_BK'),
                central_widget.parent().update_slider_value('temp_REG_BK')  # Update slider for BK
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_REGHLT': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_REG_ON_OFF_HLT_COORDINATES,
            size=constants_gui.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback(instance, 'IMG_REGHLT_Selected', 'TXT_REG_HLT'),
                central_widget.parent().update_slider_value('temp_REG_HLT')  # Update slider for HLT
            ),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_sidebar_graphs': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_SIDEBAR_GRAPHS_BUTTON,
            size=constants_gui.BTN_SIDEBAR_MENU,
            on_normal_click=show_graph_screen_callback,
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_sidebar_settings': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_SIDEBAR_ACTIVE_BUTTON_SETTINGS_COORDINATES,
            size=constants_gui.BTN_SIDEBAR_MENU,
            on_normal_click=show_settings_screen_callback,
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_set_slider_0': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_SLIDER_SET_MIN_COORDINATES,
            size=constants_gui.BTN_SLIDER_SET_MINMAX,
            on_normal_click=lambda: central_widget.parent().set_slider_value(0),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_set_slider_100': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_SLIDER_SET_MAX_COORDINATES,
            size=constants_gui.BTN_SLIDER_SET_MINMAX,
            on_normal_click=lambda: central_widget.parent().set_slider_value(100),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_quit': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_QUIT_COORDINATES,
            size=constants_gui.BTN_QUIT,
            on_normal_click=lambda: perform_shutdown(),
            on_long_click=None,
            invisible=Common.constants.BTN_INVISIBILITY
        )
    }
    return buttons

def toggle_pot_handle_all(pot_name, state = None):
    """
    Encapsulates the actions that occur when a long press happens on a pot button (BK or HLT).

    Parameters:
    - pot_name: A string, either "BK" or "HLT".
    """
    # Access the module-level references
    global _gui_static_elements, _gui_dynamic_elements, _gui_toggle_images_visibility_callback
    play_audio("Sound_Toggle.mp3", volume = 1, override_bruce = True)

    if state is not None:
        set_images_visibility(_gui_static_elements, [f'IMG_Pot_{pot_name}_On_Background', f'IMG_Pot_{pot_name}_On_Foreground'], state)
        print(f"toggle_pot_handle_all called with state ({state})")
        set_variable(f'{pot_name}_ON', STATE, state)
    else:
        _gui_toggle_images_visibility_callback(_gui_static_elements, [f'IMG_Pot_{pot_name}_On_Background', f'IMG_Pot_{pot_name}_On_Foreground'])
        toggle_variable(f'{pot_name}_ON', STATE)
    
    if pot_name == 'BK':
        handle_bk_on_toggle(_gui_dynamic_elements, _gui_static_elements)
        create_or_stop_pwm_for_bk()
    elif pot_name == 'HLT':
        handle_hlt_on_toggle(_gui_dynamic_elements, _gui_static_elements)
        create_or_stop_pwm_for_hlt()

    

def toggle_pump_handle_all(pump_name, state=None):
    """
    Encapsulates the actions that occur when a long press happens on a pump button (P1 or P2).

    Parameters:
    - pump_name: A string, either "P1" or "P2".
    - state: Optional boolean to explicitly set the pump state (True for ON, False for OFF).
    """
    # Access the module-level references
    global _gui_static_elements, _gui_dynamic_elements, _gui_toggle_images_visibility_callback
    play_audio("Sound_Toggle.mp3", volume = 1, override_bruce = True)

    if state is not None:
        set_images_visibility(_gui_static_elements,[f'IMG_Pump_On_{pump_name}'],state)
        print(f"toggle_pump_handle_all called with state ({state})")
        set_variable(f'{pump_name}_ON', STATE, state)
    else:
        _gui_toggle_images_visibility_callback(_gui_static_elements,[f'IMG_Pump_On_{pump_name}'])
        toggle_variable(f'{pump_name}_ON', STATE)

    if pump_name == 'P1':
        create_or_stop_pwm_for_p1()
        handle_p1_toggle(_gui_dynamic_elements)
    elif pump_name == 'P2':
        create_or_stop_pwm_for_p2()
        handle_p2_toggle(_gui_dynamic_elements)

def handle_bk_on_toggle(dynamic_elements, static_elements):
    if STATE['BK_ON']:
        dynamic_elements['TXT_EFFICIENCY_BK'].show()
        if variables.active_variable == 'efficiency_BK':
            set_label_text_color(dynamic_elements['TXT_EFFICIENCY_BK'], "black")
        else:
            set_label_text_color(dynamic_elements['TXT_EFFICIENCY_BK'], "white")
    else:
        dynamic_elements['TXT_EFFICIENCY_BK'].hide()
        if 'IMG_Pot_BK_On_Temp_Reached' in static_elements:
            static_elements['IMG_Pot_BK_On_Temp_Reached'].hide()

def handle_hlt_on_toggle(dynamic_elements, static_elements):
    if STATE['HLT_ON']:
        dynamic_elements['TXT_EFFICIENCY_HLT'].show()
        if variables.active_variable == 'efficiency_HLT':
            set_label_text_color(dynamic_elements['TXT_EFFICIENCY_HLT'], "black")
        else:
            set_label_text_color(dynamic_elements['TXT_EFFICIENCY_HLT'], "white")
    else:
        dynamic_elements['TXT_EFFICIENCY_HLT'].hide()
        if 'IMG_Pot_HLT_On_Temp_Reached' in static_elements:
            static_elements['IMG_Pot_HLT_On_Temp_Reached'].hide()

def handle_p1_toggle(dynamic_elements):
    from Common.variables import active_variable
    if STATE['P1_ON'] and active_variable == 'pump_speed_P1':
        set_label_text_color(dynamic_elements['TXT_PUMP_SPEED_P1'], "black")
    else:
        set_label_text_color(dynamic_elements['TXT_PUMP_SPEED_P1'], "white")

def handle_p2_toggle(dynamic_elements):
    from Common.variables import active_variable
    if STATE['P2_ON'] and active_variable == 'pump_speed_P2':
        set_label_text_color(dynamic_elements['TXT_PUMP_SPEED_P2'], "black")
    else:
        set_label_text_color(dynamic_elements['TXT_PUMP_SPEED_P2'], "white")

def create_or_stop_pwm_for_bk():
    """
    Create or stop the PWM signal for BK based on the state.
    """
    if STATE['BK_ON']:
        if variables.BK_PWM is None:  # Create PWM only if it doesn't exist
            variables.BK_PWM = set_pwm_signal(
                pin_number=constants_rpi.RPI_GPIO_PWN_BK,  
                frequency=constants_rpi.PWM_FREQUENCY,  
                duty_cycle=variables.efficiency_BK  
            )
    else:
            stop_pwm_signal(variables.BK_PWM)
            variables.BK_PWM = None

def create_or_stop_pwm_for_hlt():
    """
    Create or stop the PWM signal for HLT based on the state.
    """
    if STATE['HLT_ON']:
        if variables.HLT_PWM is None:  # Create PWM only if it doesn't exist
            variables.HLT_PWM = set_pwm_signal(
                pin_number=constants_rpi.RPI_GPIO_PWN_HLT,  
                frequency=constants_rpi.PWM_FREQUENCY,  
                duty_cycle=variables.efficiency_HLT  
            )
    else:
            stop_pwm_signal(variables.HLT_PWM)
            variables.HLT_PWM = None

def create_or_stop_pwm_for_p1():
    """
    Create or stop the software PWM signal for P1 based on the state.
    """
    if STATE['P1_ON']:
        if variables.P1_PWM is None:  # Create PWM only if it doesn't exist
            variables.P1_PWM = create_software_pwm(
                pin_number=constants_rpi.RPI_GPIO_PIN_P1,
                frequency=constants_rpi.PWM_FREQUENCY
            )
            if variables.P1_PWM:  # Start PWM with initial duty cycle
                variables.P1_PWM.start(variables.pump_speed_P1)
    else:
        if variables.P1_PWM:
            stop_pwm_signal(variables.P1_PWM)
            variables.P1_PWM = None

def create_or_stop_pwm_for_p2():
    """
    Create or stop the software PWM signal for P2 based on the state.
    """
    if STATE['P2_ON']:
        if variables.P2_PWM is None:  # Create PWM only if it doesn't exist
            variables.P2_PWM = create_software_pwm(
                pin_number=constants_rpi.RPI_GPIO_PIN_P2,
                frequency=constants_rpi.PWM_FREQUENCY
            )
            if variables.P2_PWM:  # Start PWM with initial duty cycle
                variables.P2_PWM.start(variables.pump_speed_P2)
    else:
        if variables.P2_PWM:
            stop_pwm_signal(variables.P2_PWM)
            variables.P2_PWM = None

def hide_GUI_elements(static_elements, dynamic_elements, buttons):
    """
    Hides specific static images initialized in the static GUI.

    Parameters:
    - static_elements: Dictionary of static elements in the GUI.
    """
    # Pot on gradients
    keys_to_hide = [
        'IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground', 'IMG_Pot_BK_On_Temp_Reached',
        'IMG_Pot_MLT_On_Background', 'IMG_Pot_MLT_On_Foreground',
        'IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground', 'IMG_Pot_HLT_On_Temp_Reached',
        'IMG_BK_Selected', 'IMG_HLT_Selected', 'IMG_P1_Selected', 'IMG_P2_Selected',
        'IMG_REGBK_Selected', 'IMG_REGHLT_Selected',
        'TXT_Slider_0', 'TXT_Slider_100', 'IMG_Pump_On_P1','IMG_Pump_On_P2', 'TXT_EFFICIENCY_BK', 'TXT_EFFICIENCY_HLT'

    ]
    for key in keys_to_hide:
        if key in static_elements:
            static_elements[key].hide()
        elif key in dynamic_elements:
            dynamic_elements[key].hide()
    
    # Hide slider set buttons
    button_keys_to_hide = ['BTN_set_slider_0', 'BTN_set_slider_100']
    for key in button_keys_to_hide:
        if key in buttons:
            buttons[key].hide()

    # Pot and Pump Names
    keys_to_show = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_MLT', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2']
    for key in keys_to_show:
        if key in static_elements:
            static_elements[key].show()

def set_pot_toggle_references(static_elems, dynamic_elems, toggle_images_visibility_cb):
    """
    Store references to the static and dynamic elements, as well as the toggle_images_visibility_callback,
    so we can use them in toggle_pot_handle_all without passing them as parameters each time.
    """
    global _gui_static_elements, _gui_dynamic_elements, _gui_toggle_images_visibility_callback
    _gui_static_elements = static_elems
    _gui_dynamic_elements = dynamic_elems
    _gui_toggle_images_visibility_callback = toggle_images_visibility_cb
