from PyQt5.QtWidgets import QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFontMetrics, QFontDatabase, QFont, QIcon
from PyQt5 import QtWidgets, QtCore
import os

def create_label(parent_widget, text, color='white', size=40, center=(0, 0), width=None, height=None, alignment=Qt.AlignCenter):
    """
    Creates and returns a QLabel with specified text, color, size, and alignment at a fixed center point.
    """
    # Load the custom font
    custom_font = load_custom_font()

    # Create the label
    label = QLabel(parent_widget)
    label.setText(text)

    # Set the font size and custom font
    if custom_font:
        custom_font.setPointSize(size)
        custom_font.setWeight(QFont.ExtraBold)  # Make the font bold
        label.setFont(custom_font)

    # Calculate text dimensions dynamically
    metrics = QFontMetrics(label.font())
    if width is None:
        width = metrics.horizontalAdvance("999°") + 30  # Fixed width based on the longest text
    if height is None:
        height = metrics.height() + 10  # Add padding for height

    # Calculate top-left position to center the label at the desired point
    x = center[0] - width // 2
    y = center[1] - height // 2

    # Set the position and size of the label
    label.setGeometry(x, y, width, height)

    # Set the style for colors and background
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

    print("successfully created image: ", image_path)

    return image_label
    
def create_slider(parent_widget, orientation=Qt.Horizontal, minimum=0, maximum=100, value=50, location=(0, 0), size=(200, 40), style=None):
    """
    Creates and returns a QSlider with specified properties.

    Parameters:
    parent_widget (QWidget): The widget to which the slider will be added.
    orientation (Qt.Orientation): The orientation of the slider (default is Qt.Horizontal).
    minimum (int): The minimum value of the slider (default is 0).
    maximum (int): The maximum value of the slider (default is 100).
    value (int): The initial value of the slider (default is 50).
    location (tuple): A tuple (x, y) representing the location of the slider. Default is (0, 0).
    size (tuple): A tuple (width, height) representing the size of the slider. Default is (200, 40).
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
                height: 40px;
                background: #F58361; /* The color of the unselected portion */
                border-radius: 20px;
            }
            QSlider::sub-page:horizontal {
                border: none;
                height: 40px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #F04C65, stop:1 #F58361);
                border-radius: 20px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: none;
                width: 10px;
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
        pixmap = QtGui.QPixmap(absolute_path)

        # Use the size of the image if specified
        button.setGeometry(position[0], position[1], pixmap.width(), pixmap.height())
        button.setIcon(QtGui.QIcon(pixmap))
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
                background: transparent;
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.1); /* Slightly visible when pressed */
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
    print("Toggling visibility")
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
    if font_id == -1:
        print(f"Failed to load the Cascadia Code Bold font from {font_path}.")
        return None

    # Retrieve the font family and create the font object
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    return QFont(font_family)
