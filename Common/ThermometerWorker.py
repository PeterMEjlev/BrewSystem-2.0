from PyQt5.QtCore import QObject, QThread, pyqtSignal
import Common.constants as constants
from Common.utils import adjust_image_height
from Common.constants_gui import POT_ON_FOREGROUND_HEIGHT
import Common.variables as variables
import Common.constants_rpi as constants_rpi
from Common.utils_rpi import read_ds18b20
from datetime import datetime

class ThermometerWorker(QObject):
    temperature_updated_bk = pyqtSignal(float)  # Signal to send the temperature reading
    temperature_updated_mlt = pyqtSignal(float)
    temperature_updated_hlt = pyqtSignal(float)
    finished = pyqtSignal()  # Signal to indicate the thread is finished

    def __init__(self, static_elements):
        super().__init__()
        self._running = True  # Control the thread execution
        self.static_elements = static_elements  # Store static elements for access
        self.temperature_history = []

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Read and update temperature values
            variables.temp_BK = self.read_thermometer_bk()
            variables.temp_MLT = self.read_thermometer_hlt()
            variables.temp_HLT = self.read_thermometer_hlt()
            self.temperature_updated_bk.emit(variables.temp_BK) 
            self.temperature_updated_mlt.emit(variables.temp_MLT) 
            self.temperature_updated_hlt.emit(variables.temp_HLT) 

            self.record_current_time_and_temp()

            # Calculate temperature progress for BK and HLT
            temp_progress_bk = min(100, max(0, (variables.temp_BK / variables.temp_REG_BK) * 100)) if variables.temp_REG_BK > 0 else 0
            temp_progress_hlt = min(100, max(0, (variables.temp_HLT / variables.temp_REG_HLT) * 100)) if variables.temp_REG_HLT > 0 else 0

            # Adjust image height dynamically
            if 'IMG_Pot_BK_On_Foreground' in self.static_elements:  
                adjust_image_height(self.static_elements['IMG_Pot_BK_On_Foreground'], temp_progress_bk, POT_ON_FOREGROUND_HEIGHT)
            if 'IMG_Pot_HLT_On_Foreground' in self.static_elements:  
                adjust_image_height(self.static_elements['IMG_Pot_HLT_On_Foreground'], temp_progress_hlt, POT_ON_FOREGROUND_HEIGHT)

            # Update temperature-reached visuals
            self.update_pot_foregrounds_if_temp_reached()

            # Wait for the next reading
            QThread.msleep(constants.THERMOMETER_READ_WAIT_TIME)

    def read_thermometer_bk(self):
        return read_ds18b20(constants_rpi.DS18B20_BK)  
    
    def read_thermometer_mlt(self):
        return read_ds18b20(constants_rpi.DS18B20_MLT)  

    def read_thermometer_hlt(self):
        return read_ds18b20(constants_rpi.DS18B20_HLT)  
    
    def stop(self):
        """Stop the worker loop."""
        self._running = False

    def update_temp_reached_element(self, temp, temp_reg, state, element, threshold):
        """Update visibility of temperature-reached elements."""
        if state:
            if temp >= 100 and temp_reg == 100:
                element.show()
            elif abs(temp - temp_reg) <= threshold:
                element.show()
            else:
                element.hide()
        else:
            element.hide()

    def update_pot_foregrounds_if_temp_reached(self):
        """Update the pot foregrounds if the temperature is reached."""
        if 'IMG_Pot_BK_On_Temp_Reached' in self.static_elements:
            self.update_temp_reached_element(
                variables.temp_BK,
                variables.temp_REG_BK,
                variables.STATE['BK_ON'],
                self.static_elements['IMG_Pot_BK_On_Temp_Reached'],
                constants.TEMP_REACHED_THRESHOLD
            )

        if 'IMG_Pot_HLT_On_Temp_Reached' in self.static_elements:
            self.update_temp_reached_element(
                variables.temp_HLT,
                variables.temp_REG_HLT,
                variables.STATE['HLT_ON'],
                self.static_elements['IMG_Pot_HLT_On_Temp_Reached'],
                constants.TEMP_REACHED_THRESHOLD
            )

    def record_current_time_and_temp(self):
         # Record the current time and temperature readings
            current_time = datetime.now()
            self.temperature_history.append({
                "time": current_time,
                "bk": variables.temp_BK,
                "mlt": variables.temp_MLT,
                "hlt": variables.temp_HLT
            })
