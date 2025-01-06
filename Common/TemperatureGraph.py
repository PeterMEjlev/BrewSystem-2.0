# TemperatureGraph.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
from bokeh.plotting import figure
from bokeh.io import push_notebook, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components, file_html
from bokeh.resources import CDN

class TemperatureGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.temperature_history = []  # Initialize an empty history list
        self.start_time = None  # Store the time of the first reading

        


