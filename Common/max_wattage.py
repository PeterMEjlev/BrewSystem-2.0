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

def calculate_max_new_efficiency(pot):
    if pot == "efficiency_BK":
        HLT_power = (variables.efficiency_HLT/100)*HLT_MAX_POWER
        available_power = MAX_WATTAGE - HLT_power
        max_power_bk = (available_power / BK_MAX_POWER) * 100
        return max(0, min(100, max_power_bk))
    
    if pot == "efficiency_HLT":
        BK_power = (variables.efficiency_BK/100)*BK_MAX_POWER
        available_power = MAX_WATTAGE - BK_power
        max_power_hlt = (available_power / HLT_MAX_POWER) * 100
        return max(0, min(100, max_power_hlt))
        
