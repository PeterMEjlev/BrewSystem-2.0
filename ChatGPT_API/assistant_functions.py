#assistant_functions.py
import sys, os

try:
    import Common.variables as variables
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Common import variables
except:
    pass

def toggle_pot(pot, state):
    print(f"Toggling {pot} to {state}.")
    return f"Successfully toggled {pot} to {state}."

def set_reg_temperature(pot, temperature):
    print(f"Setting {pot} to {temperature}°C.")
    if pot == 'BK':
        variables.temp_REG_BK = temperature
    elif pot == 'HLT':
        variables.temp_REG_HLT = temperature

    return f"Regulation temperature for {pot} set to {temperature}°C."