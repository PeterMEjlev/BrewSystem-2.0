# max_wattage.py
import variables as variables

MAX_WATTAGE = 10560
HLT_MAX_POWER = 5500
BK_MAX_POWER = 8500

def calculate_total_power_consumption():
    BK_current_power = (variables.efficiency_BK/100)*BK_MAX_POWER
    HLT_current_power = (variables.efficiency_HLT/100)*HLT_MAX_POWER
    total_power_consumption = BK_current_power + HLT_current_power

    return total_power_consumption

