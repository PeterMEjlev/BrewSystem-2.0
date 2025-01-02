# ThermometerWorker.py
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time, random
import Common.constants as constants
from Common.utils import adjust_image_height
from Common.constants_gui import POT_ON_FOREGROUND_HEIGHT
import Common.variables as variables


class ThermometerWorker(QObject):
    temperature_updated = pyqtSignal(float)  # Signal to send the temperature reading
    finished = pyqtSignal()  # Signal to indicate the thread is finished

    def __init__(self, static_elements):
        super().__init__()
        self._running = True  # Control the thread execution
        self.static_elements = static_elements  # Store static elements for access

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Simulate temperature reading (replace this with actual thermometer code)
            temp_BK = self.read_thermometer()
            self.temperature_updated.emit(temp_BK)  # Emit the new temperature

            print(f"Temperature: {temp_BK}")
            print(f"REG Temperature: {variables.temp_REG_BK}")

            temp_progress_bk = min(100, max(0, (temp_BK / variables.temp_REG_BK) * 100))

            # Adjust image height dynamically based on a condition or logic
            if 'IMG_Pot_BK_On_Foreground' in self.static_elements:
                
                adjust_image_height(self.static_elements['IMG_Pot_BK_On_Foreground'], temp_progress_bk, POT_ON_FOREGROUND_HEIGHT)

            QThread.msleep(constants.THERMOMETER_READ_WAIT_TIME)

    def read_thermometer(self):
        """Simulate reading temperature. Replace with actual thermometer logic."""
        return random.uniform(0.0, 101.9)  # Simulated temperature

    def stop(self):
        """Stop the worker loop."""
        self._running = False
