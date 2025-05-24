import json
import os
from dataclasses import dataclass, field
from typing import List

# File path for settings.json
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

@dataclass
class Settings:
    # JSON-backed settings
    voice: str = "normal"
    temp_REG_BK: float = 85
    temp_REG_HLT: float = 70
    efficiency_BK: float = 100
    efficiency_HLT: float = 36
    pump_speed_P1: float = 100
    pump_speed_P2: float = 100
    near_target_heating_efficiency: float = 35
    target_temp_margin: float = 1
    thermometor_read_frequency: int = 500
    average_temp_time_window: int = 10
    muted: bool = True
    BK_Boil_Timer_Threshold: int = 99
    chatGPT_assistant_keywords: List[str] = field(default_factory=list)
    webpage_poll_interval: int = 5000 # in milliseconds

    @classmethod
    def load(cls, path: str = SETTINGS_FILE) -> "Settings":
        with open(path, "r") as f:
            data = json.load(f)
        return cls(
            voice=data.get("voice", "normal"),
            temp_REG_BK=data.get("REG starting temperature BK", 85),
            temp_REG_HLT=data.get("REG starting temperature HLT", 70),
            efficiency_BK=data.get("starting efficiency BK", 100),
            efficiency_HLT=data.get("starting efficiency HLT", 36),
            pump_speed_P1=data.get("starting efficiency P1", 100),
            pump_speed_P2=data.get("starting efficiency P2", 100),
            near_target_heating_efficiency=data.get("near_target_heating_efficiency", 35),
            target_temp_margin=data.get("target_temp_margin", 1),
            thermometor_read_frequency=data.get("thermometor_read_frequency", 500),
            average_temp_time_window=data.get("average_temp_time_window", 10),
            muted=data.get("muted", True),
            BK_Boil_Timer_Threshold=data.get("BK_Boil_Timer_Threshold", 99),
            chatGPT_assistant_keywords=data.get("chatGPT_assistant_keywords", []),
            webpage_poll_interval=data.get("webpage_poll_interval", 5000)
        )

# load settings
settings = Settings.load()

# Runtime defaults and variables
# Temperatures
temp_BK = 100
temp_MLT = 68
temp_HLT = 70

temp_progress_BK = 0
temp_progress_HLT = 0

# PWM outputs
BK_PWM = None
HLT_PWM = None

# Temperature control flags
set_temp_reached_BK = False
set_temp_reached_HLT = False

# Pump speeds (initialized from settings)
pump_speed_P1 = settings.pump_speed_P1
pump_speed_P2 = settings.pump_speed_P2
P1_PWM = None
P2_PWM = None

# Active Units
STATE = {
    "BK_ON": False,
    "HLT_ON": False,
    "P1_ON": False,
    "P2_ON": False,
}

# Regulator states
BK_REG_ON = False
HLT_REG_ON = True

# ChatGPT API
talking_with_chat = False

# Currently-selected variable (e.g. slider focus)
active_variable = None

timer_progress_MLT = 0
timer_progress_BK = 0
