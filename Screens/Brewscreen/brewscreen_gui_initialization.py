# gui_initialization.py
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
import Common.constants
from Common.utils import create_slider, create_label, create_button, toggle_variable
from Common.utils_rpi import set_pwm_signal, stop_pwm_signal, create_software_pwm
from Common.variables import STATE
from Common.constants import SLIDER_PAGESTEP
import Common.constants_rpi as constants_rpi
import Common.constants_gui as constants_gui
import Common.variables as variables
from Common.shutdown import perform_shutdown




def initialize_slider(central_widget, constants, on_slider_change_callback, dynamic_elements):
    """
    Initializes the slider, its value label, and a fake slider to visually represent dynamic width.
    """
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
    slider.setPageStep(SLIDER_PAGESTEP)  # Set the page step to 1 instead of the default 10
    slider.hide()  # Start with the slider hidden
    slider.valueChanged.connect(on_slider_change_callback)

    # Create background for the fake slider
    fake_slider_background = QtWidgets.QFrame(central_widget)
    fake_slider_background.setGeometry(
        constants_gui.SLIDER_COORDINATES[0],  # Same X as the real slider
        constants_gui.SLIDER_COORDINATES[1] + 15,
        int(constants_gui.SLIDER_SIZE[0]),  # Initial width based on 50% value
        constants_gui.SLIDER_SIZE[1] + 10  # Same height as the real slider
    )
    fake_slider_background.setStyleSheet("""
        background-color: #292728; /* Solid color for the fake slider */
        border-radius: 20px;
    """)
    fake_slider_background.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    fake_slider_background.hide()

    # Create the fake slider
    fake_slider = QtWidgets.QFrame(central_widget)
    fake_slider.setGeometry(
        constants_gui.SLIDER_COORDINATES[0],  # Same X as the real slider
        constants_gui.SLIDER_COORDINATES[1] + 15,
        int(constants_gui.SLIDER_SIZE[0] * 0.5),  # Initial width based on 50% value
        constants_gui.SLIDER_SIZE[1] + 10  # Same height as the real slider
    )
    fake_slider.setStyleSheet("""
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #F04C65, stop:1 #F58361); /* Gradient for the fake slider */
        border-radius: 20px;
    """)
    fake_slider.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    fake_slider.hide()

    # Retrieve the slider value label from dynamic_elements
    value_label = dynamic_elements.get('TXT_SLIDER_VALUE', None)

    return slider, value_label, fake_slider, fake_slider_background

def initialize_buttons(central_widget, static_elements, dynamic_elements, toggle_images_visibility_callback, select_button_callback, show_graph_screen_callback, show_settings_screen_callback):
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
    buttons = {
        'BTN_toggle_BK': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_POT_BK_COORDINATES,
            size=constants_gui.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_BK_Selected', 'TXT_EFFICIENCY_BK'),
                central_widget.parent().update_slider_value('efficiency_BK')  # Update slider for BK
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground']),
                toggle_variable('BK_ON', STATE),
                handle_bk_on_toggle(dynamic_elements, static_elements),
                create_or_stop_pwm_for_bk()
            ),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_HLT': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_POT_HLT_COORDINATES,
            size=constants_gui.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_HLT_Selected', 'TXT_EFFICIENCY_HLT'),
                central_widget.parent().update_slider_value('efficiency_HLT')  # Update slider for HLT
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground']),
                toggle_variable('HLT_ON', STATE),
                handle_hlt_on_toggle(dynamic_elements, static_elements),
                create_or_stop_pwm_for_hlt()
            ),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_P1': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_PUMP_BOX_P1_COORDINATES,
            size=constants_gui.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P1_Selected', 'TXT_P1'),
                central_widget.parent().update_slider_value('pump_speed_P1')  # Update slider for P1
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pump_On_P1']),
                toggle_variable('P1_ON', STATE),
                create_or_stop_pwm_for_p1()
            ),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_P2': create_button(
            parent_widget=central_widget,
            position=constants_gui.IMG_PUMP_BOX_P2_COORDINATES,
            size=constants_gui.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P2_Selected', 'TXT_P2'),
                central_widget.parent().update_slider_value('pump_speed_P2')  # Update slider for P2
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pump_On_P2']),
                toggle_variable('P2_ON', STATE),
                create_or_stop_pwm_for_p2()               
            ),
            invisible=Common.constants.BTN_INVISIBILITY
        ),
        'BTN_toggle_REGBK': create_button(
            parent_widget=central_widget,
            position=constants_gui.BTN_REG_ON_OFF_BK_COORDINATES,
            size=constants_gui.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGBK_Selected', 'TXT_REG_BK'),
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
                select_button_callback('IMG_REGHLT_Selected', 'TXT_REG_HLT'),
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

def handle_bk_on_toggle(dynamic_elements, static_elements):
    if STATE['BK_ON']:
        dynamic_elements['TXT_EFFICIENCY_BK'].show()
    else:
        dynamic_elements['TXT_EFFICIENCY_BK'].hide()
        if 'IMG_Pot_BK_On_Temp_Reached' in static_elements:
            static_elements['IMG_Pot_BK_On_Temp_Reached'].hide()

def handle_hlt_on_toggle(dynamic_elements, static_elements):
    if STATE['HLT_ON']:
        dynamic_elements['TXT_EFFICIENCY_HLT'].show()
    else:
        dynamic_elements['TXT_EFFICIENCY_HLT'].hide()
        if 'IMG_Pot_HLT_On_Temp_Reached' in static_elements:
            static_elements['IMG_Pot_HLT_On_Temp_Reached'].hide()

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
