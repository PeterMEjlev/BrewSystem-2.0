from Common.utils import set_label_text_color, apply_gradient_to_label
import Common.variables as variables


def reset_all_gradients_and_colour(self):
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
        set_label_text_color(self.dynamic_elements[label_key], "white")
        self.dynamic_elements[label_key].update()

def apply_selection_styles(self, selected_key: str) -> None:
    """
    Apply the appropriate styles or gradients based on the selected button.

    Parameters:
    - selected_key: The key of the selected button.

    Returns:
    None
    """
    if selected_key == 'IMG_BK_Selected':
        if variables.STATE['BK_ON']:
            set_label_text_color(self.dynamic_elements['TXT_EFFICIENCY_BK'], "black")
        else:
            apply_gradient_to_label(self, selected_key)

    elif selected_key == 'IMG_HLT_Selected':
        if variables.STATE['HLT_ON']:
            set_label_text_color(self.dynamic_elements['TXT_EFFICIENCY_HLT'], "black")
        else:
            apply_gradient_to_label(self, selected_key)

    elif selected_key == 'IMG_P1_Selected':
        if variables.STATE['P1_ON']:
            set_label_text_color(self.dynamic_elements['TXT_PUMP_SPEED_P1'], "black")
        else:
            apply_gradient_to_label(self, selected_key)

    elif selected_key == 'IMG_P2_Selected':
        if variables.STATE['P2_ON']:
            set_label_text_color(self.dynamic_elements['TXT_PUMP_SPEED_P2'], "black")
        else:
            apply_gradient_to_label(self, selected_key)

    else:
        apply_gradient_to_label(self, selected_key)

def update_slider_elements(self, selected_key: str) -> None:
        """
        Update the slider elements based on the selected button.

        Parameters:
        - selected_key: The key of the selected button.

        Returns:
        None
        """
        self.show_slider_elements()

        # Update visibility of efficiency labels based on selection
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