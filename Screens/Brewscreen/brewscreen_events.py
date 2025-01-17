import Common.variables as variables
import Screens.Brewscreen.brewscreen_helpers as brewscreen_helpers
from Common.utils import set_label_text_color

def select_button(instance, selected_key, name_key):
    if instance.current_selection == selected_key:
        deselect_button(instance, selected_key, name_key)
    else:
        select_new_button(instance, selected_key, name_key)

def deselect_button(instance, selected_key, name_key):
    instance.hide_element(selected_key)
    instance.show_element(name_key)
    instance.current_selection = None
    instance.hide_slider_elements()
    brewscreen_helpers.reset_all_gradients_and_colour(instance)
    instance.reset_active_variable()

    if selected_key == 'IMG_BK_Selected':
        if not variables.STATE['BK_ON']:
            instance.dynamic_elements['TXT_EFFICIENCY_BK'].hide()
        else:
            set_label_text_color(instance.dynamic_elements['TXT_EFFICIENCY_BK'], "white")
    elif selected_key == 'IMG_HLT_Selected':
        if not variables.STATE['HLT_ON']:
            instance.dynamic_elements['TXT_EFFICIENCY_HLT'].hide()
        else:
            set_label_text_color(instance.dynamic_elements['TXT_EFFICIENCY_HLT'], "white")
    elif selected_key == 'IMG_P1_Selected':
        set_label_text_color(instance.dynamic_elements['TXT_PUMP_SPEED_P1'], "white")
    elif selected_key == 'IMG_P2_Selected':
        set_label_text_color(instance.dynamic_elements['TXT_PUMP_SPEED_P2'], "white")
 
def select_new_button(instance, selected_key: str, name_key: str) -> None:
    """
    Handles the logic when a new button is selected.

    Parameters:
    - selected_key: The key of the selected button (e.g., 'IMG_BK_Selected').
    - name_key: The associated name key for the selected button.

    Returns:
    None
    """
    if instance.current_selection == selected_key:
        # If already selected, reset state and return
        instance.reset_current_selection()
        return

    # Reset gradients and prepare for new selection
    brewscreen_helpers.reset_all_gradients_and_colour(instance)

    # Update active variable based on the selected button
    instance.update_active_variable_for_selection(selected_key)
    print(f"Active variable updated to: {instance.active_variable}")

    # Apply styles or gradients to the selected button
    brewscreen_helpers.apply_selection_styles(instance, selected_key)

    # Update slider elements and visibility
    brewscreen_helpers.update_slider_elements(instance, selected_key)

    # Update current selection
    instance.current_selection = selected_key