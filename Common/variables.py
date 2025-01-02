# variables.py

# Temperatures
temp_BK = 100
temp_MLT = 68
temp_HLT = 70

temp_progress_BK = 0
temp_progress_HLT = 0

# Efficiency
efficiency_BK = 100
efficiency_HLT = 100
BK_PWM = None
HLT_PWM = None

# REG values
temp_REG_BK = 85
temp_REG_HLT = 70

# Pump speeds
pump_speed_P1 = 100
pump_speed_P2 = 100

# Active Units
STATE = {
    'BK_ON': False,
    'HLT_ON': False,
    'P1_ON': False,
    'P2_ON': False,
}

active_variable = None


