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
        self._update_toggle = False

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Read and update temperature values
            variables.temp_BK = self.read_thermometer_bk()
            variables.temp_MLT = self.read_thermometer_mlt()
            variables.temp_HLT = self.read_thermometer_hlt()

            # Unified temperature-reached checks
            self.check_if_reg_temp_reached('BK')
            self.check_if_reg_temp_reached('HLT')

            self.control_pwm_output()

            # Emit updated temperatures
            if variables.temp_BK  >= 0: self.temperature_updated_bk.emit(variables.temp_BK)
            if variables.temp_MLT >= 0: self.temperature_updated_mlt.emit(variables.temp_MLT)
            if variables.temp_HLT >= 0: self.temperature_updated_hlt.emit(variables.temp_HLT)

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

            # only call update_graph every OTHER loop (~ every 1 second)
            self._update_toggle = not self._update_toggle
            if self._update_toggle:
                self.graph.update_graph(variables.temp_BK,
                                        variables.temp_MLT,
                                        variables.temp_HLT)

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

    def check_if_reg_temp_reached(self, key):
        """Generic check for BK/HLT reaching target temperature."""
        temp = getattr(variables, f"temp_{key}")
        reg = getattr(variables, f"temp_REG_{key}")
        set_flag = f"set_temp_reached_{key}"
        m = constants.TEMP_REACHED_MARGIN
        r = constants.TEMP_RESET_MARGIN

        if reg - m <= temp <= reg + m:
            if not getattr(variables, set_flag):
                setattr(variables, set_flag, True)
                play_audio(f"{key}_set_temp_reached - Male.mp3")
                change_pwm_duty_cycle(getattr(constants_rpi, f"RPI_GPIO_PWN_{key}"), 0)
        else:
            if getattr(variables, set_flag) and (temp < reg - r or temp > reg + r):
                setattr(variables, set_flag, False)

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

    def control_pwm_output(self):
        """Control the PWM output for BK and HLT using dynamic max wattage management."""
        margin = constants.TEMP_REACHED_MARGIN
        near_target_heating_efficiency = constants.NEAR_TARGET_HEATING_EFFICIENCY

        # BK control
        if variables.STATE['BK_ON'] and variables.BK_REG_ON:
            self._apply_pwm_control('BK', variables.temp_BK, variables.temp_REG_BK, margin, near_target_heating_efficiency)

        # HLT control
        if variables.STATE['HLT_ON'] and variables.HLT_REG_ON:
            # limit to 35% near target for HLT
            self._apply_pwm_control('HLT', variables.temp_HLT, variables.temp_REG_HLT, margin, 35)

    def _apply_pwm_control(self, key, temp, reg, margin, max_eff_limit):
        flag = getattr(variables, f"efficiency_{key}")
        if temp >= reg:
            change_pwm_duty_cycle(getattr(constants_rpi, f"RPI_GPIO_PWN_{key}"), 0)
            self.variable_updated.emit(f"efficiency_{key}", 0)
            setattr(variables, f"efficiency_{key}", 0)
        elif temp >= reg - margin:
            new_eff = min(max_eff_limit, Common.max_wattage.calculate_max_new_efficiency(f"efficiency_{key}"))
            change_pwm_duty_cycle(getattr(constants_rpi, f"RPI_GPIO_PWN_{key}"), new_eff)
            self.variable_updated.emit(f"efficiency_{key}", new_eff)
            setattr(variables, f"efficiency_{key}", new_eff)
        else:
            new_eff = Common.max_wattage.calculate_max_new_efficiency(f"efficiency_{key}" )
            change_pwm_duty_cycle(getattr(constants_rpi, f"RPI_GPIO_PWN_{key}"), new_eff)
            self.variable_updated.emit(f"efficiency_{key}", new_eff)
            setattr(variables, f"efficiency_{key}", new_eff)
