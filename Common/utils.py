# utils.py
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFontMetrics, QFontDatabase, QFont, QIcon, QLinearGradient, QBrush, QPainter, QPen, QColor
from Common.utils_rpi import set_gpio_high, set_gpio_low
import Common.constants_rpi as constants_rpi
from PyQt5 import QtWidgets, QtCore
import os

def create_label(parent_widget, text, color='white', gradient_colors=None, size=40, center=(0, 0), width=None, height=None, alignment=Qt.AlignCenter):
    """
    Creates and returns a QLabel with specified text, color, size, and alignment at a fixed center point.

    If gradient_colors is provided (a tuple of two colors), the text will be rendered with a gradient.
    """

    class GradientLabel(QLabel):
        def __init__(self, text, gradient_colors, *args, **kwargs):
            super().__init__(text, *args, **kwargs)
            self.gradient_colors = gradient_colors

        def paintEvent(self, event):
            if self.gradient_colors:
                painter = QPainter(self)
                gradient = QLinearGradient(0, 0, self.width(), 0)  # Horizontal gradient
                gradient.setColorAt(0.0, QColor(self.gradient_colors[0]))  # Convert start color to QColor
                gradient.setColorAt(1.0, QColor(self.gradient_colors[1]))  # Convert end color to QColor
                brush = QBrush(gradient)

                pen = QPen(brush, 0)  # Use gradient as pen
                painter.setPen(pen)
                painter.setFont(self.font())
                painter.drawText(self.rect(), self.alignment(), self.text())
            else:
                super().paintEvent(event)

    # Load the custom font
    custom_font = load_custom_font()

    # Create the label
    label = GradientLabel(text, gradient_colors, parent_widget)

    # Set the font size and custom font
    if custom_font:
        custom_font.setPointSize(size)
        custom_font.setWeight(QFont.ExtraBold)  # Make the font bold
        label.setFont(custom_font)

    # Calculate text dimensions dynamically
    metrics = QFontMetrics(label.font())
    if width is None:
        width = metrics.horizontalAdvance("110.10°") + 30  # Fixed width based on the longest text
    if height is None:
        height = metrics.height() + 10  # Add padding for height

    # Calculate top-left position to center the label at the desired point
    x = center[0] - width // 2
    y = center[1] - height // 2

    # Set the position and size of the label
    label.setGeometry(x, y, width, height)

    # Set the style for background and alignment
    label.setStyleSheet("background-color: transparent; margin: 0px; padding: 0px;")

    # Set the style for plain text
    if not gradient_colors:
        label.setStyleSheet(f"""
            color: {color};
            background-color: transparent;
            margin: 0px;
            padding: 0px;
        """)

    # Apply alignment
    label.setAlignment(alignment)

    # Make the label transparent to mouse events
    label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    return label

def apply_gradient_to_label(self, selected_key):
        """
        Apply a gradient to the label associated with the selected key.

        Parameters:
        selected_key (str): The key of the selected element.
        """
        label_mapping = {
            'IMG_BK_Selected': 'TXT_EFFICIENCY_BK',
            'IMG_HLT_Selected': 'TXT_EFFICIENCY_HLT',
            'IMG_REGBK_Selected': 'TXT_TEMP_REG_BK',
            'IMG_REGHLT_Selected': 'TXT_TEMP_REG_HLT',
            'IMG_P1_Selected': 'TXT_PUMP_SPEED_P1',
            'IMG_P2_Selected': 'TXT_PUMP_SPEED_P2'
        }

        label_key = label_mapping.get(selected_key)
        if label_key and label_key in self.dynamic_elements:
            self.dynamic_elements[label_key].gradient_colors = ('#D04158', '#F58360')
            self.dynamic_elements[label_key].update()  # Force the label to redraw

def create_image(parent_widget, image_path, center=(0, 0), size=None):
    """
    Creates and returns a QLabel with an image displayed, respecting transparency.

    Parameters:
    parent_widget (QWidget): The widget to which the image will be added.
    image_path (str): The relative path or filename of the image in the Assets folder.
    location (tuple): A tuple (x, y) representing the location of the image. Default is (0, 0).
    size (tuple): A tuple (width, height) to resize the image. Default is None (original size).

    Returns:
    QLabel: The configured QLabel object displaying the image.
    """
    # Automatically resolve the image path relative to the Assets folder
    base_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
    absolute_path = os.path.join(base_path, image_path)

    # Create the QLabel
    image_label = QLabel(parent_widget)

    # Load the image
    pixmap = QPixmap(absolute_path)

    # Resize the image if size is specified
    if size:
        pixmap = pixmap.scaled(size[0], size[1], aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

    # Set the pixmap on the label
    image_label.setPixmap(pixmap)

    # Set the position and size of the label
    width = pixmap.width() if not size else size[0]
    height = pixmap.height() if not size else size[1]
    image_label.setGeometry(center[0], center[1], width, height)

    # Ensure transparency of the image
    image_label.setAttribute(Qt.WA_TranslucentBackground)
    image_label.setStyleSheet("background: transparent;")

    return image_label
    
def create_slider(parent_widget, orientation=Qt.Horizontal, minimum=0, maximum=100, value=50, location=(0, 0), size=(200, 70), style=None):
    """
    Creates and returns a QSlider with specified properties.

    Parameters:
    parent_widget (QWidget): The widget to which the slider will be added.
    orientation (Qt.Orientation): The orientation of the slider (default is Qt.Horizontal).
    minimum (int): The minimum value of the slider (default is 0).
    maximum (int): The maximum value of the slider (default is 100).
    value (int): The initial value of the slider (default is 50).
    location (tuple): A tuple (x, y) representing the location of the slider. Default is (0, 0).
    size (tuple): A tuple (width, height) representing the size of the slider. Default is (200, 70).
    style (str): A string containing the custom stylesheet for the slider (default is None).

    Returns:
    QSlider: The configured QSlider object.
    """
    # Create the slider
    slider = QSlider(orientation, parent_widget)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)
    slider.setValue(value)

    # Set the position and size of the slider
    slider.setGeometry(location[0], location[1], size[0], size[1])
    slider.setMinimumHeight(70)  # Ensure the widget is tall enough to accommodate the larger handle

    # Apply the custom style if provided
    if style:
        slider.setStyleSheet(style)
    else:
        # Default style
        slider.setStyleSheet("""
            QSlider {
                background: transparent; /* Make the slider background transparent */
            }
            QSlider::groove:horizontal {
                border: none;
                height: 40px; /* Set the slider bar height */
                background: transparent; 
                border-radius: 20px;
            }
            QSlider::sub-page:horizontal {
                border: none;
                height: 40px; /* Match the slider bar height */
                background: transparent;
                border-radius: 20px;
            }
            QSlider::handle:horizontal {
                background-color: transparent; /* Handle color */
                border: none;
                height: 50px; /* Increase handle height */
                width: 75px; /* Increase handle width */
                margin: -15px 0; /* Ensure handle extends above and below groove */
                border-radius: 10px; /* Make handle circular */
            }
            
        """)

    return slider
  
def create_button(parent_widget, position=(0, 0), size=(100, 50), image_path=None,
                  on_normal_click=None, on_long_click=None, invisible=False, long_click_duration=300):
    """
    Creates and returns a QPushButton with specified properties.

    Parameters:
    parent_widget (QWidget): The widget to which the button will be added.
    position (tuple): A tuple (x, y) representing the position of the button.
    size (tuple): A tuple (width, height) representing the size of the button.
                  If image_path is provided, the image size is used.
    image_path (str): The relative path to an image for the button background. Default is None.
    on_normal_click (function): The function to activate on a normal click. Default is None.
    on_long_click (function): The function to activate on a long click. Default is None.
    invisible (bool): Whether the button should be invisible while still functional. Default is False.
    long_click_duration (int): Duration in milliseconds to detect a long click. Default is 1000ms.

    Returns:
    QPushButton: The configured QPushButton object.
    """
    class CustomButton(QtWidgets.QPushButton):
        normal_clicked = QtCore.pyqtSignal()
        long_clicked = QtCore.pyqtSignal()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.long_click_timer = QtCore.QTimer()
            self.long_click_timer.setSingleShot(True)
            self.long_click_timer.setInterval(long_click_duration)
            self.long_click_timer.timeout.connect(self._trigger_long_click)

            self.is_long_click = False  # Track if a long click occurred

            # Connect signals to provided callbacks
            if on_normal_click:
                self.normal_clicked.connect(on_normal_click)
            if on_long_click:
                self.long_clicked.connect(on_long_click)

        def mousePressEvent(self, event):
            # Start the long-click timer on press
            self.is_long_click = False
            self.long_click_timer.start()
            super().mousePressEvent(event)

        def mouseReleaseEvent(self, event):
            # If the timer is active, it means the press was short (normal click)
            if self.long_click_timer.isActive():
                self.long_click_timer.stop()
                if not self.is_long_click:
                    self.normal_clicked.emit()
            super().mouseReleaseEvent(event)

        def _trigger_long_click(self):
            # Mark as long click and emit the signal
            self.is_long_click = True
            self.long_clicked.emit()

    # Create the custom button
    button = CustomButton(parent_widget)
    button.setGeometry(position[0], position[1], size[0], size[1])

    # Set an image for the button if provided
    if image_path:
        base_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        absolute_path = os.path.join(base_path, image_path)
        pixmap = QPixmap(absolute_path)

        # Use the size of the image if specified
        button.setGeometry(position[0], position[1], pixmap.width(), pixmap.height())
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.size())

    # Set styles based on invisibility
    if invisible:
        button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:pressed {
                background: transparent;
                border: none;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
    else:
        button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 105, 180, 0.5); /* Hot Pink */
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.15); /* Slightly visible when pressed */
            }
        """)

    return button

def toggle_images_visibility(static_elements, image_keys):
    """
    Toggles the visibility of one or more images.

    Parameters:
    static_elements (dict): Dictionary containing the static elements (e.g., images).
    image_keys (list): List of keys for the images in the static_elements dictionary.
    """
    for key in image_keys:
        if key in static_elements:
            element = static_elements[key]
            if element.isVisible():
                element.hide()
            else:
                element.show()

def load_custom_font():
    """
    Loads the Cascadia Code Bold font from a .ttf file and sets it as the default font.
    """
    # Use the bold font file
    font_path = os.path.join(os.path.dirname(__file__), "CascadiaCode.ttf")
    
    # Add the font to the application
    font_id = QFontDatabase.addApplicationFont(font_path)

    # Retrieve the font family and create the font object
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    return QFont(font_family)

def toggle_variable(variable_name, globals_dict):
    """
    Toggles the value of a variable between True and False, and updates the GPIO state.

    Parameters:
    - variable_name (str): The name of the variable to toggle.
    - globals_dict (dict): The dictionary of global variables to search for the variable.

    Returns:
    - None
    """
    if variable_name in globals_dict:
        current_value = globals_dict[variable_name]
        if isinstance(current_value, bool):  # Ensure it's a boolean before toggling
            # Toggle the variable
            globals_dict[variable_name] = not current_value
            new_value = globals_dict[variable_name]
            print(f"{variable_name} toggled to {new_value}")

            # Call the separate GPIO state update function
            update_gpio_state(variable_name, new_value)
        else:
            print(f"{variable_name} is not a boolean. Current value: {current_value}")
    else:
        print(f"{variable_name} does not exist in the provided scope.")


def adjust_image_height(image_label, percentage, original_height):
    """
    Adjust the height of an image based on a percentage of a given original height without maintaining the aspect ratio,
    ensuring the height is reduced or increased from the top-center of the image.

    Parameters:
    - image_label (QLabel): The QLabel displaying the image.
    - percentage (float): The percentage (0.0 to 100.0) to adjust the height.
                          A value of 100 means the original height.
    - original_height (int): The reference height for the percentage calculation.
    """
    if not isinstance(image_label, QLabel) or image_label.pixmap() is None:
        print("Invalid image label or no pixmap set.")
        return

    # Get the original pixmap and its width
    pixmap = image_label.pixmap()
    original_width = pixmap.width()

    # Calculate the new height based on the percentage and given original height
    new_height = int(original_height * (percentage / 100.0))
    if new_height <= 0:
        print("Invalid percentage: height cannot be zero or negative.")
        return

    # Resize the pixmap to the original width and the new height
    resized_pixmap = pixmap.scaled(original_width, new_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    # Set the resized pixmap back to the label
    image_label.setPixmap(resized_pixmap)

    # Calculate the new position for the QLabel to keep the top-center alignment
    current_geometry = image_label.geometry()
    new_top = current_geometry.top() + (current_geometry.height() - new_height)
    image_label.setGeometry(current_geometry.left(), new_top, resized_pixmap.width(), resized_pixmap.height())

def update_gpio_state(variable_name, new_value):
    """
    Updates the GPIO state based on the variable name.

    Parameters:
    - variable_name (str): The name of the variable to check.
    - new_value (bool): The new value of the variable (True or False).
    """
    if variable_name == 'BK_ON':  # Example: BK corresponds to the BK GPIO pin
        if new_value:
            set_gpio_high(constants_rpi.RPI_GPIO_PIN_BK)
        else:
            set_gpio_low(constants_rpi.RPI_GPIO_PIN_BK)

    elif variable_name == 'HLT_ON':  # Example: HLT corresponds to the HLT GPIO pin
        if new_value:
            set_gpio_high(constants_rpi.RPI_GPIO_PIN_HLT)
        else:
            set_gpio_low(constants_rpi.RPI_GPIO_PIN_HLT)
    
    elif variable_name == 'P1_ON':
        if new_value:
            set_gpio_high(constants_rpi.RPI_GPIO_PIN_P1)
        else:
            set_gpio_low(constants_rpi.RPI_GPIO_PIN_P1)

    elif variable_name == 'P2_ON':
        if new_value:
            set_gpio_high(constants_rpi.RPI_GPIO_PIN_P2)
        else:
            set_gpio_low(constants_rpi.RPI_GPIO_PIN_P2)

    else:
        print(f"No GPIO action defined for {variable_name}.")

def set_opacity(widget, opacity):
    """
    Set the opacity of a widget.

    Parameters:
    - widget: The widget to which the opacity effect will be applied.
    - opacity: The desired opacity level (0.0 to 1.0).
    """
    effect = QGraphicsOpacityEffect()
    effect.setOpacity(opacity)
    widget.setGraphicsEffect(effect)