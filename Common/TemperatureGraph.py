# TemperatureGraph.py
# TemperatureGraph.py
from pyqtgraph import PlotWidget, mkPen, AxisItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from datetime import datetime


class TemperatureGraph(QWidget):
    def __init__(self, parent=None, width=1520, height=1050, x_pos=420, y_pos=0):
        super().__init__(parent)
        self.temperature_history = []  # Initialize an empty history list
        self.start_time = None  # Store the time of the first reading


    def update_graph(self, temp_bk, temp_mlt, temp_hlt):
        """Update the graph with new temperature data."""
        # Capture the current timestamp
        current_time = datetime.now()

        # Initialize the start time if this is the first reading
        if self.start_time is None:
            self.start_time = current_time

        # Calculate elapsed time in seconds since the start
        elapsed_time = (current_time - self.start_time).total_seconds()

        # Append new temperature data to history with the elapsed time
        self.temperature_history.append({
            "time": elapsed_time,  # Store elapsed time as x-axis value
            "bk": temp_bk,
            "mlt": temp_mlt,
            "hlt": temp_hlt
        })

        # Extract data for plotting
        times = [entry["time"] for entry in self.temperature_history]
        bk_temps = [entry["bk"] for entry in self.temperature_history]
        mlt_temps = [entry["mlt"] for entry in self.temperature_history]
        hlt_temps = [entry["hlt"] for entry in self.temperature_history]

        # Update the plot lines
        self.bk_line.setData(times, bk_temps)
        self.mlt_line.setData(times, mlt_temps)
        self.hlt_line.setData(times, hlt_temps)
