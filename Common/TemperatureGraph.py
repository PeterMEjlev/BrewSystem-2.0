# TemperatureGraph.py
from pyqtgraph import PlotWidget, mkPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from datetime import datetime

class TemperatureGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.temperature_history = []  # Initialize an empty history list

    def init_ui(self):
        layout = QVBoxLayout()
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground("w")  # White background
        self.plot_widget.addLegend()

        # Set up the plot lines for temperatures
        self.bk_line = self.plot_widget.plot(pen=mkPen(color="r", width=2), name="BK Temperature")
        self.mlt_line = self.plot_widget.plot(pen=mkPen(color="g", width=2), name="MLT Temperature")
        self.hlt_line = self.plot_widget.plot(pen=mkPen(color="b", width=2), name="HLT Temperature")

        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def update_graph(self, temp_bk, temp_mlt, temp_hlt):
        """Update the graph with new temperature data."""
        # Append new temperature data to history with a timestamp
        self.temperature_history.append({
            "timestamp": datetime.now(),
            "bk": temp_bk,
            "mlt": temp_mlt,
            "hlt": temp_hlt
        })

        # Extract data for plotting
        timestamps = [entry["timestamp"].strftime("%H:%M:%S") for entry in self.temperature_history]
        bk_temps = [entry["bk"] for entry in self.temperature_history]
        mlt_temps = [entry["mlt"] for entry in self.temperature_history]
        hlt_temps = [entry["hlt"] for entry in self.temperature_history]

        # Update the plot lines
        self.bk_line.setData(list(range(len(timestamps))), bk_temps)
        self.mlt_line.setData(list(range(len(timestamps))), mlt_temps)
        self.hlt_line.setData(list(range(len(timestamps))), hlt_temps)
