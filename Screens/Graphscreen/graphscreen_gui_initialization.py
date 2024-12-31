# graphscreen_gui_initialization.py
from Screens.Graphscreen.graphscreen_static_gui import initialize_static_elements
from Common.utils import create_button

def initialize_gui_elements(parent_widget, assets_path):
    """
    Initializes GUI elements for the GraphScreen.

    Parameters:
    - parent_widget: The widget to which the elements are added.
    - assets_path: The path to the assets directory.
    """
    if not assets_path:
        raise ValueError("Assets path is not set. Ensure `assets_path` is correctly initialized.")

    # Initialize static elements
    parent_widget.static_elements = initialize_static_elements(parent_widget, assets_path)

    # Explicitly show all elements
    for key, element in parent_widget.static_elements.items():
        print(f"Static Element: {key}, Is Visible: {element.isVisible()}")
        element.show()

    # Initialize buttons
    parent_widget.buttons = initialize_buttons(parent_widget)


def initialize_buttons(parent_widget):
    """
    Initializes buttons for the GraphScreen.

    Parameters:
    - parent_widget: The widget to which the button is added.

    Returns:
    A dictionary containing the button(s).
    """
    buttons = {
        'BTN_Show_Plot': create_button(
            parent_widget=parent_widget, position=(100, 100),  
            size=(200, 50), 
            on_normal_click=lambda: print("Show Plot button clicked!"), 
            on_long_click=None,
            invisible=False
        )
    }

    # Show the button explicitly
    for button in buttons.values():
        button.show()

    return buttons
