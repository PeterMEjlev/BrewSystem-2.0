from pyqtgraph import PlotWidget, mkPen, AxisItem, ViewBox
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
from datetime import datetime
import numpy as np
from collections import deque
from Common.constants import GRAPH_LINE_WIDTH


class TemperatureGraph(QWidget):
    def __init__(self, parent=None, width=1420, height=950, x_pos=400, y_pos=0):
        super().__init__(parent)
        self.width = width  # Graph width
        self.height = height  # Graph height
        self.x_pos = x_pos  # Graph x position
        self.y_pos = y_pos  # Graph y position

        # Keep an internal history (1 Hz logging) and redraw skip counter
        self.temperature_history = []  # Stores all entries every second
        self._redraw_skip = 0         # Only redraw every 5 updates
        self.start_time = None        # Time of the first reading

        self.init_ui()

    def init_ui(self):
        # Create custom axes for white color and larger text
        left_axis = AxisItem(orientation='left')
        bottom_axis = AxisItem(orientation='bottom')

        # Customize the axis appearance
        font = QFont()
        font.setPointSize(18)  # Set font size for axis ticks
        font.setBold(True)
        font.setWeight(75)

        # Apply the font to axis ticks
        left_axis.setStyle(tickFont=font, tickTextOffset=10)
        bottom_axis.setStyle(tickFont=font, tickTextOffset=10)
        left_axis.setPen(mkPen(color='white', width=2))
        bottom_axis.setPen(mkPen(color='white', width=2))

        # Set overall widget size and position
        self.setFixedSize(self.width + self.x_pos, self.height + self.y_pos)
        self.plot_widget = PlotWidget(self, axisItems={'left': left_axis, 'bottom': bottom_axis})
        self.plot_widget.setBackground("#3E3E3F")
        self.plot_widget.setFixedSize(self.width, self.height)
        self.plot_widget.move(self.x_pos, self.y_pos)
        self.plot_widget.showGrid(x=False, y=True, alpha=0.08)

        # Style for axis labels
        label_style = {
            'color': 'white',
            'font-size': f"{font.pointSize()}pt",
            'font-weight': 'bold'
        }

        # Fixed x- and y-range
        #self.plot_widget.setYRange(0, 100)
        vb = self.plot_widget.getViewBox()
        vb.setLimits(xMin=0)
        self.plot_widget.setLabel("left", "Temperature (°C)", **label_style)
        # Label bottom in minutes now
        self.plot_widget.setLabel("bottom", "Time (min)", **label_style)

        # Initialize plot lines with clickable interaction
        self.bk_line  = self.plot_widget.plot(pen=mkPen(color="r", width=GRAPH_LINE_WIDTH), name="BK Temperature", connect="finite", clickable=True)
        self.mlt_line = self.plot_widget.plot(pen=mkPen(color="g", width=GRAPH_LINE_WIDTH), name="MLT Temperature", connect="finite", clickable=True)
        self.hlt_line = self.plot_widget.plot(pen=mkPen(color="b", width=GRAPH_LINE_WIDTH), name="HLT Temperature", connect="finite", clickable=True)

        # Connect click signals
        self.bk_line.sigClicked.connect(lambda item, points: self.show_point_info(item, points, "BK"))
        self.mlt_line.sigClicked.connect(lambda item, points: self.show_point_info(item, points, "MLT"))
        self.hlt_line.sigClicked.connect(lambda item, points: self.show_point_info(item, points, "HLT"))

    def update_graph(self, temp_bk, temp_mlt, temp_hlt):
        """Update the graph with new temperature data."""
        current_time = datetime.now()

        if self.start_time is None:
            self.start_time = current_time

        # Convert elapsed time to minutes
        elapsed_min = (current_time - self.start_time).total_seconds() / 60.0

        # Log every second
        entry = {
            "time": elapsed_min,
            "bk":  temp_bk  if temp_bk  >= 0 else np.nan,
            "mlt": temp_mlt if temp_mlt >= 0 else np.nan,
            "hlt": temp_hlt if temp_hlt >= 0 else np.nan,
        }
        self.temperature_history.append(entry)

        # Only redraw the plot every 5 logged points (~every 5 seconds)
        self._redraw_skip += 1
        if self._redraw_skip < 5:
            return
        self._redraw_skip = 0

        # Extract data for plotting
        times     = [e["time"] for e in self.temperature_history]
        bk_temps  = [e["bk"]   for e in self.temperature_history]
        mlt_temps = [e["mlt"]  for e in self.temperature_history]
        hlt_temps = [e["hlt"]  for e in self.temperature_history]

        # Redraw with auto-downsample to improve performance
        self.bk_line .setData(times, bk_temps,  autoDownsample=True, downsampleMethod='mean')
        self.mlt_line.setData(times, mlt_temps, autoDownsample=True, downsampleMethod='mean')
        self.hlt_line.setData(times, hlt_temps, autoDownsample=True, downsampleMethod='mean')

    def zoom_in(self, axis="y"):
        view_range   = self.plot_widget.getViewBox().viewRange()
        current_range = view_range[0] if axis == "x" else view_range[1]
        center       = (current_range[0] + current_range[1]) / 2
        new_range    = [(center - (center - current_range[0]) * 0.8), (center + (current_range[1] - center) * 0.8)]
        if axis == "x":
            self.plot_widget.setXRange(*new_range)
        else:
            self.plot_widget.setYRange(*new_range)

    def zoom_out(self, axis="y"):
        view_range   = self.plot_widget.getViewBox().viewRange()
        current_range = view_range[0] if axis == "x" else view_range[1]
        center       = (current_range[0] + current_range[1]) / 2
        new_range    = [(center - (center - current_range[0]) * 1.25), (center + (current_range[1] - center) * 1.25)]
        if axis == "x":
            self.plot_widget.setXRange(*new_range)
        else:
            self.plot_widget.setYRange(*new_range)

    def enable_auto_range(self, axis="both"):
        from pyqtgraph import ViewBox
        if axis == "x":
            self.plot_widget.getViewBox().enableAutoRange(axis=ViewBox.XAxis)
        elif axis == "y":
            self.plot_widget.getViewBox().enableAutoRange(axis=ViewBox.YAxis)
        else:
            self.plot_widget.getViewBox().enableAutoRange()

    def toggle_line_visibility(self, line_name):
        if line_name == "bk":
            self.bk_line.setVisible(not self.bk_line.isVisible())
        elif line_name == "mlt":
            self.mlt_line.setVisible(not self.mlt_line.isVisible())
        elif line_name == "hlt":
            self.hlt_line.setVisible(not self.hlt_line.isVisible())
        else:
            raise ValueError(f"Invalid line_name: {line_name}. Must be 'bk', 'mlt', or 'hlt'.")

    def show_point_info(self, item, event, line_name):
        mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
        x_clicked, y_clicked = mouse_point.x(), mouse_point.y()
        x_data, y_data       = item.getData()
        closest_index        = (np.abs(np.array(x_data) - x_clicked)).argmin()
        x_closest, y_closest = x_data[closest_index], y_data[closest_index]

        if not hasattr(self, 'info_label'):
            self.info_label = QLabel(self.plot_widget)
            self.info_label.setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.1); color: white; padding: 10px; border-radius: 5px; font-size: 30px;"
            )
            self.info_label.setAlignment(QLabel.AlignCenter)

        self.info_label.setText(f"{line_name}: {y_clicked:.2f} °C")
        self.info_label.adjustSize()
        self.info_label.move(int(event.scenePos().x()), int(event.scenePos().y()) - 40)
        self.info_label.show()
        QTimer.singleShot(3000, self.info_label.hide)
