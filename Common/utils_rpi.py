from Common.config import IS_RPI
import random, time, os
import Common.constants_rpi as constants_rpi

if IS_RPI:
    import pigpio
    pi = pigpio.pi()
else:
    pi = None

_pwm_objects = {}

def set_gpio_high(pin_number):
    if IS_RPI:
        try:
            pi.write(pin_number, 1)
            print(f"GPIO pin {pin_number} set to HIGH.")
        except Exception as e:
            print(f"Error setting GPIO pin {pin_number} HIGH: {e}")
    else:
        print(f"GPIO pin {pin_number} set to HIGH (simulated).")

def set_gpio_low(pin_number):
    if IS_RPI:
        try:
            pi.write(pin_number, 0)
            print(f"GPIO pin {pin_number} set to LOW.")
        except Exception as e:
            print(f"Error setting GPIO pin {pin_number} LOW: {e}")
    else:
        print(f"GPIO pin {pin_number} set to LOW (simulated).")

def set_pwm_signal(pin_number, frequency, duty_cycle):
    if IS_RPI:
        try:
            pi.set_mode(pin_number, pigpio.OUTPUT)
            duty_hw = int((duty_cycle / 100) * 1_000_000)
            try:
                pi.hardware_PWM(pin_number, frequency, duty_hw)
                _pwm_objects[pin_number] = ('hardware', frequency)
                print(f"Started **hardware** PWM on pin {pin_number}, freq={frequency}Hz, duty={duty_cycle}%.")
            except pigpio.error:
                print(f"Hardware PWM not available on pin {pin_number}, falling back to software PWM.")
                pi.set_PWM_frequency(pin_number, frequency)
                pi.set_PWM_range(pin_number, 100)
                pi.set_PWM_dutycycle(pin_number, duty_cycle)
                _pwm_objects[pin_number] = ('software', frequency)
                print(f"Started **software** PWM on pin {pin_number}, freq={frequency}Hz, duty={duty_cycle}%.")
            return pin_number  # ⬅️ Just return the pin number
        except Exception as e:
            print(f"Failed to start PWM on pin {pin_number}: {e}")
            return None
    else:
        print(f"PWM started on pin {pin_number} (simulated), freq={frequency}, duty={duty_cycle}%.")
        return pin_number

def stop_pwm_signal(pin_number):
    if IS_RPI and pin_number in _pwm_objects:
        mode, _ = _pwm_objects[pin_number]
        try:
            if mode == 'hardware':
                pi.hardware_PWM(pin_number, 0, 0)
            elif mode == 'software':
                pi.set_PWM_dutycycle(pin_number, 0)
            print(f"Stopped {mode} PWM on pin {pin_number}.")
            _pwm_objects.pop(pin_number, None)
        except Exception as e:
            print(f"Error stopping PWM on pin {pin_number}: {e}")
    else:
        print(f"PWM stopped on pin {pin_number} (simulated or not started).")

def change_pwm_duty_cycle(pin_number, duty_cycle):
    if IS_RPI and pin_number in _pwm_objects:
        mode, frequency = _pwm_objects[pin_number]
        try:
            if mode == 'hardware':
                duty_hw = int((duty_cycle / 100) * 1_000_000)
                pi.hardware_PWM(pin_number, frequency, duty_hw)
            elif mode == 'software':
                pi.set_PWM_dutycycle(pin_number, duty_cycle)
            print(f"{mode.capitalize()} PWM duty cycle on pin {pin_number} changed to {duty_cycle}%.")
        except Exception as e:
            print(f"Error changing PWM duty cycle on pin {pin_number}: {e}")
    else:
        print(f"PWM duty cycle change simulated on pin {pin_number}.")

def initialize_ds18b20_resolution(serial_code, resolution="9"):
    if IS_RPI:
        sensor_dir = f"/sys/bus/w1/devices/{serial_code}"
        resolution_file = os.path.join(sensor_dir, "resolution")
        if os.path.exists(resolution_file):
            try:
                with open(resolution_file, "w") as f:
                    f.write(resolution)
                print(f"Sensor {serial_code} resolution set to {resolution}-bit.")
            except Exception as e:
                print(f"Warning: Unable to set sensor {serial_code} resolution: {e}")
        else:
            print(f"Resolution file for sensor {serial_code} not found.")

def read_ds18b20(serial_code):
    if IS_RPI:
        sensor_file_path = f"/sys/bus/w1/devices/{serial_code}/w1_slave"
        start_time = time.time()
        try:
            with open(sensor_file_path, 'r') as f:
                lines = f.readlines()

            if lines[0].strip()[-3:] != "YES":
                raise ValueError("CRC check failed.")

            temp_output = lines[1].split("t=")
            if len(temp_output) < 2:
                raise ValueError("Temperature data not found.")
            temp_c = float(temp_output[1]) / 1000.0
            end_time = time.time()
            print(f"read_ds18b20 time: {end_time - start_time:.3f}s")
            return temp_c
        except FileNotFoundError:
            return -1.0
        except Exception as e:
            print(f"Error reading DS18B20: {e}")
            return -1.0
    else:
        return random.uniform(35.0, 102.0)

def initialize_gpio():
    if IS_RPI:
        try:
            pins = [
                constants_rpi.RPI_GPIO_PIN_BK,
                constants_rpi.RPI_GPIO_PIN_HLT,
                constants_rpi.RPI_GPIO_PWN_BK,
                constants_rpi.RPI_GPIO_PWN_HLT,
                constants_rpi.RPI_GPIO_PIN_P1,
                constants_rpi.RPI_GPIO_PIN_P2
            ]
            for pin in pins:
                pi.set_mode(pin, pigpio.OUTPUT)
                pi.write(pin, 0)
            print("GPIO pins initialized with pigpio.")
        except Exception as e:
            print(f"Error initializing GPIO with pigpio: {e}")
    else:
        print("GPIO initialization skipped (simulated).")
