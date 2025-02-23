# max_wattage.py
import Common.variables as variables

MAX_WATTAGE = 10560
HLT_MAX_POWER = 5500
BK_MAX_POWER = 8500

def calculate_current_total_power_consumption():
    BK_current_power = (variables.efficiency_BK/100)*BK_MAX_POWER
    HLT_current_power = (variables.efficiency_HLT/100)*HLT_MAX_POWER
    total_power_consumption = BK_current_power + HLT_current_power

    return total_power_consumption

def calculate_new_total_power_consumption(pot, new_value):
    if pot == "efficiency_BK":
        BK_new_power = (new_value/100)*BK_MAX_POWER
        HLT_new_power = (variables.efficiency_HLT/100)*HLT_MAX_POWER
    elif pot == "efficiency_HLT":
        BK_new_power = (variables.efficiency_BK/100)*BK_MAX_POWER
        HLT_new_power = (new_value/100)*HLT_MAX_POWER

    total_new_power_consumption = BK_new_power + HLT_new_power
    return total_new_power_consumption

def power_is_within_limit(power):
    if power < MAX_WATTAGE:
        return True
    else:
        return False

