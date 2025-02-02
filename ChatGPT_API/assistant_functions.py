#assistant_functions.py
import sys, os
from Screens.Brewscreen.brewscreen_gui_initialization import toggle_pot_handle_all, toggle_pump_handle_all

try:
    import Common.variables as variables
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Common import variables
except:
    pass

def toggle_pot(pot, state):
    #print(f"toggle_pot: Toggling {pot} to {state}.")
    toggle_pot_handle_all(pot, state)
    return f"Successfully toggled {pot} to {state}."

def set_pot_efficiency(pot, efficiency):
    print(f"set_pot_efficiency: Setting {pot} efficiency to {efficiency}.")
    return f"Successfully set {pot} efficiency to {efficiency}."

def set_reg_temperature(pot, temperature):
    print(f"set_reg_temperature: Setting {pot} to {temperature}°C.")
    if pot == 'BK':
        variables.temp_REG_BK = temperature
    elif pot == 'HLT':
        variables.temp_REG_HLT = temperature

    return f"Regulation temperature for {pot} set to {temperature}°C."

def toggle_pump(pump, state):
    toggle_pump_handle_all(pump, state)
    return f"Successfully toggled {pump} to {state}."

def set_pump_efficiency(pump, efficiency):
    print(f"set_pump_efficiency: Setting {pump} efficiency to {efficiency}.")
    return f"Successfully set {pump} efficiency to {efficiency}."