# IMPORT LIBRARIES
import os
from time import sleep

import RPi.GPIO as GPIO

# LOAD ENVIRONMENT VARIABLES
MAX_TEMP = int(os.getenv('MAX_TEMP'))
MIN_TEMP = int(os.getenv('MIN_TEMP'))
INTERVAL = int(os.getenv('INTERVAL'))
GPIO_PIN = int(os.getenv('GPIO_PIN'))


# CLASS FanManager()
class FanManager:
    def __init__(self):
        self.max_temp = MAX_TEMP
        self.current_temp = 0
        self.min_temp = MIN_TEMP
        self.interval = INTERVAL
        self.gpio_pin = GPIO_PIN

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def get_cpu_temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp') as file:
            self.current_temp = round(float(file.read()) / 1000, 2)


# CLASS Loop()
class Loop:
    def __init__(self):
        self.fan_manager = FanManager()

    def loop_forever(self):
        try:
            while True:
                self.fan_manager.get_cpu_temp()
                if self.fan_manager.current_temp >= MAX_TEMP:
                    GPIO.output(3, True)
                if self.fan_manager.current_temp <= MIN_TEMP:
                    GPIO.output(3, False)
                sleep(INTERVAL)
        finally:
            GPIO.cleanup()


# CALL CLASS
if __name__ == '__main__':
    l = Loop()
    l.loop_forever()
