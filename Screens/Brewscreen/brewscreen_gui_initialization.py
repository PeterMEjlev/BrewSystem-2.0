# gui_initialization.py
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
from Common.utils import create_slider, create_label, create_button, toggle_variable
from Common.variables import STATE
from Common.constants import SLIDER_PAGESTEP
import Common.gui_constants as gui_constants
from Common.utils_rpi import set_gpio_high
import Common.constants_rpi as constants



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
        location=gui_constants.SLIDER_COORDINATES,
        size=gui_constants.SLIDER_SIZE
    )
    slider.setPageStep(SLIDER_PAGESTEP)  # Set the page step to 1 instead of the default 10
    slider.hide()  # Start with the slider hidden
    slider.valueChanged.connect(on_slider_change_callback)

    # Create background for the fake slider
    fake_slider_background = QtWidgets.QFrame(central_widget)
    fake_slider_background.setGeometry(
        gui_constants.SLIDER_COORDINATES[0],  # Same X as the real slider
        gui_constants.SLIDER_COORDINATES[1] + 15,
        int(gui_constants.SLIDER_SIZE[0]),  # Initial width based on 50% value
        gui_constants.SLIDER_SIZE[1] + 10  # Same height as the real slider
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
        gui_constants.SLIDER_COORDINATES[0],  # Same X as the real slider
        gui_constants.SLIDER_COORDINATES[1] + 15,
        int(gui_constants.SLIDER_SIZE[0] * 0.5),  # Initial width based on 50% value
        gui_constants.SLIDER_SIZE[1] + 10  # Same height as the real slider
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

def initialize_buttons(central_widget, gui_constants, static_elements, toggle_images_visibility_callback, select_button_callback, show_graph_screen_callback):
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
            position=gui_constants.IMG_POT_BK_COORDINATES,
            size=gui_constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGBK_Selected', 'TXT_REG_BK'),
                central_widget.parent().update_slider_value('temp_REG_BK')  # Update slider for BK
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground']),
                toggle_variable('BK_ON', STATE)

            ),
            invisible=True
        ),
        'BTN_toggle_HLT': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_POT_HLT_COORDINATES,
            size=gui_constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGHLT_Selected', 'TXT_REG_HLT'),
                central_widget.parent().update_slider_value('temp_REG_HLT')  # Update slider for HLT
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground']),
                toggle_variable('HLT_ON', STATE)
            ),
            invisible=True
        ),
        'BTN_toggle_P1': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_PUMP_BOX_P1_COORDINATES,
            size=gui_constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P1_Selected', 'TXT_P1'),
                central_widget.parent().update_slider_value('pump_speed_P1')  # Update slider for P1
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pump_On_P1']),
                toggle_variable('P1_ON', STATE)
            ),
            invisible=True
        ),
        'BTN_toggle_P2': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_PUMP_BOX_P2_COORDINATES,
            size=gui_constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P2_Selected', 'TXT_P2'),
                central_widget.parent().update_slider_value('pump_speed_P2')  # Update slider for P2
            ),
            on_long_click=lambda: (
                toggle_images_visibility_callback(static_elements, ['IMG_Pump_On_P2']),
                toggle_variable('P2_ON', STATE)                
            ),
            invisible=True
        ),
        'BTN_toggle_REGBK': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_REG_BOX_BK_COORDINATES,
            size=gui_constants.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGBK_Selected', 'TXT_REG_BK'),
                central_widget.parent().update_slider_value('temp_REG_BK')  # Update slider for BK
            ),
            on_long_click=None,
            invisible=True
        ),
        'BTN_toggle_REGHLT': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_REG_BOX_HLT_COORDINATES,
            size=gui_constants.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGHLT_Selected', 'TXT_REG_HLT'),
                central_widget.parent().update_slider_value('temp_REG_HLT')  # Update slider for HLT
            ),
            on_long_click=None,
            invisible=True
        ),
        'BTN_toggle_sidebar_graphs': create_button(
            parent_widget=central_widget,
            position=gui_constants.IMG_SIDEBAR_GRAPHS_BUTTON,
            size=gui_constants.BTN_SIDEBAR_MENU,
            on_normal_click=show_graph_screen_callback,
            on_long_click=None,
            invisible=True
        )
    }
    return buttons

def hide_GUI_elements(static_elements):
    """
    Hides specific static images initialized in the static GUI.

    Parameters:
    - static_elements: Dictionary of static elements in the GUI.
    """
    # Pot on gradients
    keys_to_hide = [
        'IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground',
        'IMG_Pot_MLT_On_Background', 'IMG_Pot_MLT_On_Foreground',
        'IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground',
        'IMG_BK_Selected', 'IMG_HLT_Selected', 'IMG_P1_Selected', 'IMG_P2_Selected',
        'IMG_REGBK_Selected', 'IMG_REGHLT_Selected',
        'TXT_Slider_0', 'TXT_Slider_100', 'IMG_Pump_On_P1','IMG_Pump_On_P2'
    ]
    for key in keys_to_hide:
        if key in static_elements:
            static_elements[key].hide()

    # Pot and Pump Names
    keys_to_show = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_MLT', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2']
    for key in keys_to_show:
        if key in static_elements:
            static_elements[key].show()
