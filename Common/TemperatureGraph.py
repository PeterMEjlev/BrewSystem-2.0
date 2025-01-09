# TemperatureGraph.py
from pyqtgraph import PlotWidget, mkPen, AxisItem, LegendItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from datetime import datetime


class TemperatureGraph(QWidget):
    def __init__(self, parent=None, width=1420, height=950, x_pos=400, y_pos=0):
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
        #self.plot_widget.addLegend()
        

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

        # Prepare temperature data, replacing negative values with None
        entry = {
            "time": elapsed_time,  # Store elapsed time as x-axis value
            "bk": temp_bk if temp_bk >= 0 else None,  # Include only non-negative values
            "mlt": temp_mlt if temp_mlt >= 0 else None,
            "hlt": temp_hlt if temp_hlt >= 0 else None,
        }

        # Append the entry to history
        self.temperature_history.append(entry)

        # Extract data for plotting
        times = [entry["time"] for entry in self.temperature_history]
        bk_temps = [entry["bk"] for entry in self.temperature_history]
        mlt_temps = [entry["mlt"] for entry in self.temperature_history]
        hlt_temps = [entry["hlt"] for entry in self.temperature_history]

        # Update the plot lines
        self.bk_line.setData(times, bk_temps)
        self.mlt_line.setData(times, mlt_temps)
        self.hlt_line.setData(times, hlt_temps)

    def zoom_in(self, axis="y"):
        """
        Zoom in on the graph by adjusting the specified axis range.

        Parameters:
        - axis (str): The axis to zoom in on ("x" or "y").
        """
        view_range = self.plot_widget.getViewBox().viewRange()
        current_range = view_range[0] if axis == "x" else view_range[1]  # Select x-axis or y-axis range
        center = (current_range[0] + current_range[1]) / 2  # Calculate the center of the range
        new_range = [(center - (center - current_range[0]) * 0.8), 
                    (center + (current_range[1] - center) * 0.8)]  # Zoom in
        if axis == "x":
            self.plot_widget.setXRange(*new_range)
        elif axis == "y":
            self.plot_widget.setYRange(*new_range)

    def zoom_out(self, axis="y"):
        """
        Zoom out on the graph by adjusting the specified axis range.

        Parameters:
        - axis (str): The axis to zoom out on ("x" or "y").
        """
        view_range = self.plot_widget.getViewBox().viewRange()
        current_range = view_range[0] if axis == "x" else view_range[1]  # Select x-axis or y-axis range
        center = (current_range[0] + current_range[1]) / 2  # Calculate the center of the range
        new_range = [(center - (center - current_range[0]) * 1.25), 
                    (center + (current_range[1] - center) * 1.25)]  # Zoom out
        if axis == "x":
            self.plot_widget.setXRange(*new_range)
        elif axis == "y":
            self.plot_widget.setYRange(*new_range)

    def enable_auto_range(self, axis="both"):
        """
        Enables auto-range for the specified axis or both axes.

        Parameters:
        - axis (str): The axis to enable auto-range on ("x", "y", or "both").
        """
        if axis == "x":
            self.plot_widget.getViewBox().enableAutoRange(axis=ViewBox.XAxis)
        elif axis == "y":
            self.plot_widget.getViewBox().enableAutoRange(axis=ViewBox.YAxis)
        elif axis == "both":
            self.plot_widget.getViewBox().enableAutoRange()

