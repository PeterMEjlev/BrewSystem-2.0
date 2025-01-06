# TemperatureGraph.py
from pyqtgraph import PlotWidget, mkPen, AxisItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from datetime import datetime


class TemperatureGraph(QWidget):
    def __init__(self, parent=None, width=1520, height=1050, x_pos=420, y_pos=0):
        super().__init__(parent)
        self.width = width  # Graph width
        self.height = height  # Graph height
        self.x_pos = x_pos  # Graph x position
        self.y_pos = y_pos  # Graph y position
        self.init_ui()
        self.temperature_history = []  # Initialize an empty history list
        self.start_time = None  # Store the time of the first reading

    def init_ui(self):
        # Create custom axes for white color and larger text
        left_axis = AxisItem(orientation='left')
        bottom_axis = AxisItem(orientation='bottom')

        # Customize the axis appearance
        font = QFont()
        font.setPointSize(18)  # Set font size for axis ticks
        font.setBold(True)  # Set font weight to bold
        font.setWeight(75)  # Set font weight to 75
     
        # Apply the font to axis ticks
        left_axis.setStyle(tickFont=font, tickTextOffset=10)
        bottom_axis.setStyle(tickFont=font, tickTextOffset=10)
        left_axis.setPen(mkPen(color='white', width=2))  # White left axis line
        bottom_axis.setPen(mkPen(color='white', width=2))  # White bottom axis line

        self.setFixedSize(self.width + self.x_pos, self.height + self.y_pos)  # Set widget size to include graph space
        self.plot_widget = PlotWidget(self, axisItems={'left': left_axis, 'bottom': bottom_axis})
        self.plot_widget.setBackground("#3E3E3F")  # Grey background
        self.plot_widget.addLegend()

        # Adjust the size and position of the graph
        self.plot_widget.setFixedSize(self.width, self.height)  # Set graph size
        self.plot_widget.move(self.x_pos, self.y_pos)  # Adjust position (x, y)

        # Convert QFont to a dictionary for axis labels
        label_style = {
            'color': 'white',
            'font-size': f"{font.pointSize()}pt",
            'font-weight': 'bold' if font.bold() else 'normal'
        }

        # Enable axis labels and set fixed y-axis range
        self.plot_widget.setYRange(0, 100)  # Set fixed range from 0 to 100
        self.plot_widget.setLabel("left", "Temperature (°C)", **label_style)  # Use unified font for y-axis label
        self.plot_widget.setLabel("bottom", "Time (s)", **label_style)  # Use unified font for x-axis label

        # Set up the plot lines for temperatures
        self.bk_line = self.plot_widget.plot(pen=mkPen(color="r", width=2), name="BK Temperature")
        self.mlt_line = self.plot_widget.plot(pen=mkPen(color="g", width=2), name="MLT Temperature")
        self.hlt_line = self.plot_widget.plot(pen=mkPen(color="b", width=2), name="HLT Temperature")

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
