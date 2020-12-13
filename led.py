import RPi.GPIO as gpio
import time

gpio_dict = {
        'green': 33,
        'yellow': 35,
        'red': 37}
gpio.setmode(gpio.BOARD)
for k, v in gpio_dict.items():
    gpio.setup(v, gpio.OUT)

def ledLight(light_list):
    for k, v in gpio_dict.items():
        gpio.output(v, gpio.LOW)
    if len(light_list) != 0:
        for i in light_list:
            gpio.output(gpio_dict[i], gpio.HIGH)

def ledShark():
    n = 1
    for i in range(20):
        if n % 3 == 1:
            ledLight(['green'])
        elif n % 3 == 2:
            ledLight(['yellow'])
        elif n % 3 == 0:
            ledLight(['red'])
        else:
            ledLight(['green', 'yellow', 'red'])
        time.sleep(0.5)
        n += 1

if __name__ == '__main__':
    ledShark()
