from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import os

class GifViewer(QLabel):
    def __init__(self, parent, gif_name, x=0, y=0, width=100, height=100):
        """
        Initialize a GIF viewer.

        Parameters:
        - parent: QWidget parent.
        - gif_name: Name of the GIF file (e.g., "bruce_thinking.gif").
        - x, y, width, height: Position and size of the QLabel.
        """
        super().__init__(parent)
        
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: transparent;")
        self.setGeometry(x, y, width, height)

        # Determine the project's root folder based on the location of this file.
        # If gif_viewer.py is in a subfolder, ".." goes one level up to the root.
        root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        gif_path = os.path.join(root_folder, "Assets", "Gifs", gif_name)

        # Debugging: Print the resolved path and check if file exists
        print(f"Trying to load GIF from: {gif_path}")
        print(f"File exists: {os.path.exists(gif_path)}")

        # Load the GIF
        self.movie = QMovie(gif_path)

        if not self.movie.isValid():
            print("Error: Failed to load GIF")  # Debugging message

        self.setMovie(self.movie)

    def stop_gif(self):
        """Stop the GIF animation."""
        self.movie.stop()

    def start_gif(self):
        """Start the GIF animation."""
        self.movie.start()
