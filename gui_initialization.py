# gui_initialization.py
from PyQt5.QtCore import Qt
from Common.utils import create_slider, create_label, create_button


def initialize_slider(central_widget, constants, on_slider_change_callback):
    """
    Initializes the slider and its value label.

    Parameters:
    - central_widget: The parent widget for the slider.
    - constants: Constants containing slider properties.
    - on_slider_change_callback: Function to call when the slider value changes.

    Returns:
    A tuple containing the slider and its associated label.
    """
    # Add slider to the screen
    slider = create_slider(
        parent_widget=central_widget,
        orientation=Qt.Horizontal,
        minimum=constants.SLIDER_MIN,
        maximum=constants.SLIDER_MAX,
        value=50,
        location=constants.SLIDER_COORDINATES,
        size=constants.SLIDER_SIZE
    )
    slider.hide()  # Start with the slider hidden
    slider.valueChanged.connect(on_slider_change_callback)

    # Add a label to display the slider value
    value_label = create_label(
        parent_widget=central_widget,
        text=str(slider.value()),
        color='white',
        size=constants.TXT_SLIDER_VALUE_SIZE,
        center=(constants.TXT_SLIDER_VALUE_COORDINATES)
    )
    value_label.hide()  # Start with the label hidden

    return slider, value_label


def initialize_buttons(central_widget, constants, static_elements, toggle_images_visibility_callback, select_button_callback):
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
            position=constants.IMG_POT_BK_COORDINATES,
            size=constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_BK_Selected', 'TXT_POT_NAME_BK'),
                central_widget.parent().update_slider_value('temp_BK')  # Update slider for BK
            ),
            on_long_click=lambda: toggle_images_visibility_callback(static_elements, ['IMG_Pot_BK_On_Background', 'IMG_Pot_BK_On_Foreground']),
            invisible=True
        ),
        'BTN_toggle_HLT': create_button(
            parent_widget=central_widget,
            position=constants.IMG_POT_HLT_COORDINATES,
            size=constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: select_button_callback('IMG_HLT_Selected', 'TXT_POT_NAME_HLT'),
            on_long_click=lambda: toggle_images_visibility_callback(static_elements, ['IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground']),
            invisible=True
        ),
        'BTN_toggle_HLT': create_button(
            parent_widget=central_widget,
            position=constants.IMG_POT_HLT_COORDINATES,
            size=constants.BTN_POT_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_HLT_Selected', 'TXT_POT_NAME_HLT'),
                central_widget.parent().update_slider_value('temp_HLT')  # Update slider for HLT
            ),
            on_long_click=lambda: toggle_images_visibility_callback(static_elements, ['IMG_Pot_HLT_On_Background', 'IMG_Pot_HLT_On_Foreground']),
            invisible=True
        ),
        'BTN_toggle_P1': create_button(
            parent_widget=central_widget,
            position=constants.IMG_PUMP_BOX_P1_COORDINATES,
            size=constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P1_Selected', 'TXT_P1'),
                central_widget.parent().update_slider_value('pump_speed_P1')  # Update slider for P1
            ),
            on_long_click=None,
            invisible=True
        ),
        'BTN_toggle_P2': create_button(
            parent_widget=central_widget,
            position=constants.IMG_PUMP_BOX_P2_COORDINATES,
            size=constants.BTN_PUMP_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_P2_Selected', 'TXT_P2'),
                central_widget.parent().update_slider_value('pump_speed_P2')  # Update slider for P2
            ),
            on_long_click=None,
            invisible=True
        ),
        'BTN_toggle_REGBK': create_button(
            parent_widget=central_widget,
            position=constants.IMG_REG_BOX_BK_COORDINATES,
            size=constants.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGBK_Selected', 'TXT_REG_BK'),
                central_widget.parent().update_slider_value('temp_REG_BK')  # Update slider for BK
            ),
            on_long_click=None,
            invisible=True
        ),
        'BTN_toggle_REGHLT': create_button(
            parent_widget=central_widget,
            position=constants.IMG_REG_BOX_HLT_COORDINATES,
            size=constants.BTN_REG_ON_OFF,
            on_normal_click=lambda: (
                select_button_callback('IMG_REGHLT_Selected', 'TXT_REG_HLT'),
                central_widget.parent().update_slider_value('temp_REG_HLT')  # Update slider for HLT
            ),
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
        'TXT_Slider_0', 'TXT_Slider_100'
    ]
    for key in keys_to_hide:
        if key in static_elements:
            static_elements[key].hide()

    # Pot and Pump Names
    keys_to_show = ['TXT_POT_NAME_BK', 'TXT_POT_NAME_MLT', 'TXT_POT_NAME_HLT', 'TXT_P1', 'TXT_P2']
    for key in keys_to_show:
        if key in static_elements:
            static_elements[key].show()
