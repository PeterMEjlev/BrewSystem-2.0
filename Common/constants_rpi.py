# constants_rpi.py

# GPIO pin numbers for heating element SSRs (3.3V)
RPI_GPIO_PIN_BK = 17
RPI_GPIO_PIN_HLT = 18

# GPIO pin numbers for pump control
RPI_GPIO_PIN_P1 = 21
RPI_GPIO_PIN_P2 = 27

# GPIO pin numbers for heating element efficiency control (PWM)
RPI_GPIO_PWN_BK = 12 # Hardware PWM
RPI_GPIO_PWN_HLT = 13 # Hardware PWM
PWM_FREQUENCY = 1000

# GPIO pin numbers for pump efficiency control (PWM)
RPI_GPIO_PWM_P1 = 5   # Software PWM
RPI_GPIO_PWM_P2 = 6   # Software PWM

# DS18B20 sensor serial codes
DS18B20_BK = '28-00000b80089a'
DS18B20_MLT = '28-00000b81425c'
DS18B20_HLT = '28-00000b80bee4'

# DS18B20 sensor pin
DS18B20_PIN = 7