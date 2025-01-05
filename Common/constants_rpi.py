# constants_rpi.py

# GPIO pin numbers for heating element SSRs (3.3V)
RPI_GPIO_PIN_BK = 17
RPI_GPIO_PIN_HLT = 27

# GPIO pin numbers for pump control
RPI_GPIO_PIN_P1 = 22
RPI_GPIO_PIN_P2 = 23

# GPIO pin numbers for heating element efficiency control (PWM)
RPI_GPIO_PWN_BK = 12
RPI_GPIO_PWN_HLT = 13
PWM_FREQUENCY = 1000

# GPIO pin numbers for pump efficiency control (PWM)
RPI_GPIO_PWM_P1 = 5   # GPIO 5 (Pin 29)
RPI_GPIO_PWM_P2 = 6   # GPIO 6 (Pin 31)


# DS18B20 sensor serial codes
DS18B20_BK = '28-00000a3b1b58'
DS18B20_MLT = '28-00000a3b1b58'
DS18B20_HLT = '28-00000a3b1b58'
