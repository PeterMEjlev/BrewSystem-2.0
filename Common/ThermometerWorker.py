#ThermometerWorker.py
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import Common.constants as constants
from Common.utils import adjust_image_height, play_audio
from Common.constants_gui import POT_ON_FOREGROUND_HEIGHT
import Common.variables as variables
import Common.constants_rpi as constants_rpi
from Common.utils_rpi import read_ds18b20, change_pwm_duty_cycle
from Common.TemperatureGraph import TemperatureGraph
import Common.max_wattage

class ThermometerWorker(QObject):
    temperature_updated_bk = pyqtSignal(float)  # Signal to send the temperature reading
    temperature_updated_hlt = pyqtSignal(float)
    temperature_updated_mlt = pyqtSignal(float)
    variable_updated = pyqtSignal(str, int)
    finished = pyqtSignal()  # Signal to indicate the thread is finished

    def __init__(self, static_elements, graph):
        super().__init__()
        self._running = True  # Control the thread execution
        self.static_elements = static_elements  # Store static elements for access
        self.graph = graph  # Pass the graph instance to update

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Read and update temperature values
            variables.temp_BK = self.read_thermometer_bk()
            variables.temp_MLT = self.read_thermometer_mlt()
            variables.temp_HLT = self.read_thermometer_hlt()

            self.check_if_reg_temp_reached_BK()
            self.check_if_reg_temp_reached_HLT()
            
            self.control_pwm_output()
            
            if variables.temp_BK >= 0:
                self.temperature_updated_bk.emit(variables.temp_BK)
            if variables.temp_MLT >= 0:
                self.temperature_updated_mlt.emit(variables.temp_MLT)
            if variables.temp_HLT >= 0:
                self.temperature_updated_hlt.emit(variables.temp_HLT)

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

            # Update the graph
            self.graph.update_graph(variables.temp_BK, variables.temp_MLT, variables.temp_HLT)

            # Wait for the next reading
            QThread.msleep(constants.THERMOMETER_READ_FREQUENCY)

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
                constants.TEMP_REACHED_MARGIN
            )

        if 'IMG_Pot_HLT_On_Temp_Reached' in self.static_elements:
            self.update_temp_reached_element(
                variables.temp_HLT,
                variables.temp_REG_HLT,
                variables.STATE['HLT_ON'],
                self.static_elements['IMG_Pot_HLT_On_Temp_Reached'],
                constants.TEMP_REACHED_MARGIN
            )

    def check_if_reg_temp_reached_BK(self):
        temp = variables.temp_BK
        reg  = variables.temp_REG_BK
        m    = constants.TEMP_REACHED_MARGIN
        r    = constants.TEMP_RESET_MARGIN

        # 1) if we're inside the ±MARGIN band and haven't alarmed yet → alarm
        if reg - m <= temp <= reg + m:
            if not variables.set_temp_reached_BK:
                variables.set_temp_reached_BK = True
                play_audio("BK_set_temp_reached - Male.mp3")
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_BK, 0)

        # 2) if we already alarmed, only reset once we've left the wider ±RESET_MARGIN band
        else:
            if variables.set_temp_reached_BK and (temp < reg - r or temp > reg + r):
                variables.set_temp_reached_BK = False

    def check_if_reg_temp_reached_HLT(self):
        temp = variables.temp_HLT
        reg  = variables.temp_REG_HLT
        m    = constants.TEMP_REACHED_MARGIN
        r    = constants.TEMP_RESET_MARGIN

        # 1) if we're inside the ±MARGIN band and haven't alarmed yet → alarm
        if reg - m <= temp <= reg + m:
            if not variables.set_temp_reached_HLT:
                variables.set_temp_reached_HLT = True
                play_audio("HLT_set_temp_reached - Male.mp3")
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_HLT, 0)
        # 2) if we already alarmed, only reset once we've left the wider ±RESET_MARGIN band
        else:
            if variables.set_temp_reached_HLT and (temp < reg - r or temp > reg + r):
                variables.set_temp_reached_HLT = False
                 
    def control_pwm_output(self):
        """Control the PWM output for BK and HLT using dynamic max wattage management."""
        margin = constants.TEMP_REACHED_MARGIN
        near_target_heating_efficiency = constants.NEAR_TARGET_HEATING_EFFICIENCY

        # BK control
        if variables.STATE['BK_ON'] and variables.BK_REG_ON:
            temp_bk = variables.temp_BK
            reg_bk = variables.temp_REG_BK
            if temp_bk >= reg_bk:
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_BK, 0)
                self.variable_updated.emit('efficiency_BK', 0)
                variables.efficiency_BK = 0
            elif temp_bk >= reg_bk - margin:
                new_eff = min(near_target_heating_efficiency, Common.max_wattage.calculate_max_new_efficiency("efficiency_BK"))
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_BK, new_eff)
                self.variable_updated.emit('efficiency_BK', new_eff)
                variables.efficiency_BK = new_eff
            else:
                new_eff = Common.max_wattage.calculate_max_new_efficiency("efficiency_BK")
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_BK, new_eff)
                self.variable_updated.emit('efficiency_BK', new_eff)
                variables.efficiency_BK = new_eff

        # HLT control
        if variables.STATE['HLT_ON'] and variables.HLT_REG_ON:
            temp_hlt = variables.temp_HLT
            reg_hlt = variables.temp_REG_HLT
            if temp_hlt >= reg_hlt:
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_HLT, 0)
                self.variable_updated.emit('efficiency_HLT', 0)
                variables.efficiency_HLT = 0
            elif temp_hlt >= reg_hlt - margin:
                new_eff = min(35, Common.max_wattage.calculate_max_new_efficiency("efficiency_HLT"))
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_HLT, new_eff)
                self.variable_updated.emit('efficiency_HLT', new_eff)
                variables.efficiency_HLT = new_eff
            else:
                new_eff = Common.max_wattage.calculate_max_new_efficiency("efficiency_HLT")
                change_pwm_duty_cycle(constants_rpi.RPI_GPIO_PWN_HLT, new_eff)
                self.variable_updated.emit('efficiency_HLT', new_eff)
                variables.efficiency_HLT = new_eff


            
            




        
        
