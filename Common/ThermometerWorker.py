# ThermometerWorker.py
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time, random
import Common.constants as constants
from Common.utils import adjust_image_height
from Common.constants_gui import POT_ON_FOREGROUND_HEIGHT
import Common.variables as variables


class ThermometerWorker(QObject):
    temperature_updated_bk = pyqtSignal(float)  # Signal to send the temperature reading
    temperature_updated_hlt = pyqtSignal(float)
    finished = pyqtSignal()  # Signal to indicate the thread is finished

    def __init__(self, static_elements):
        super().__init__()
        self._running = True  # Control the thread execution
        self.static_elements = static_elements  # Store static elements for access

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Simulate temperature reading (replace this with actual thermometer code)
            variables.temp_BK = self.read_thermometer_bk()
            variables.temp_HLT = self.read_thermometer_hlt()
            self.temperature_updated_bk.emit(variables.temp_BK)  
            self.temperature_updated_hlt.emit(variables.temp_HLT) 

            temp_progress_bk = min(100, max(0, (variables.temp_BK / variables.temp_REG_BK) * 100))
            temp_progress_hlt = min(100, max(0, (variables.temp_HLT / variables.temp_REG_HLT) * 100))

            # Adjust image height dynamically based on a condition or logic
            if 'IMG_Pot_BK_On_Foreground' in self.static_elements:  
                adjust_image_height(self.static_elements['IMG_Pot_BK_On_Foreground'], temp_progress_bk, POT_ON_FOREGROUND_HEIGHT)
            if 'IMG_Pot_HLT_On_Foreground' in self.static_elements:  
                adjust_image_height(self.static_elements['IMG_Pot_HLT_On_Foreground'], temp_progress_hlt, POT_ON_FOREGROUND_HEIGHT)

            self.update_pot_foregrounds_if_temp_reached()


            QThread.msleep(constants.THERMOMETER_READ_WAIT_TIME)

    def read_thermometer_bk(self):
        """Simulate reading temperature. Replace with actual thermometer logic."""
        return random.uniform(0.0, 102.0)  # Simulated temperature
    
    def read_thermometer_hlt(self):
        """Simulate reading temperature. Replace with actual thermometer logic."""
        return random.uniform(0.0, 102.0)  # Simulated temperature

    def stop(self):
        """Stop the worker loop."""
        self._running = False

    def update_pot_foregrounds_if_temp_reached(self):
        """Update the pot foregrounds if the temperature is reached."""
        if 'IMG_Pot_BK_On_Temp_Reached' in self.static_elements:
                temp_reached_element_bk = self.static_elements['IMG_Pot_BK_On_Temp_Reached']
                if variables.STATE['BK_ON']:
                    temp_diff = abs(variables.temp_BK - variables.temp_REG_BK)
                    if temp_diff <= constants.TEMP_REACHED_THRESHOLD:
                        temp_reached_element_bk.show()
                    else:
                        temp_reached_element_bk.hide()
                else:
                    temp_reached_element_bk.hide()

        if 'IMG_Pot_HLT_On_Temp_Reached' in self.static_elements:
                temp_reached_element_hlt = self.static_elements['IMG_Pot_HLT_On_Temp_Reached']
                if variables.STATE['HLT_ON']:
                    temp_diff = abs(variables.temp_HLT - variables.temp_REG_HLT)
                    if temp_diff <= constants.TEMP_REACHED_THRESHOLD:
                        temp_reached_element_hlt.show()
                    else:
                        temp_reached_element_hlt.hide()
                else:
                    temp_reached_element_hlt.hide()