import RPi.GPIO as gpio
import time
import sys

gpio_list = [11, 13, 15, 16]
gpio.setmode(gpio.BOARD)
for k in gpio_list:
    gpio.setup(k, gpio.OUT)

def go(direction, value):
    print(direction)
    direction_dict = {
            'front': ([0,2], [1,3]),
            'back': ([1,3], [0,2]),
            'left': ([1,2], [0,3]),
            'right': ([0,3], [1,2])
            }
    low_list, high_list = direction_dict[direction]
    for i in low_list:
        gpio.output(gpio_list[int(i)], gpio.LOW)
    for i in high_list:
        gpio.output(gpio_list[int(i)], gpio.HIGH)
    if value == 2:
        time.sleep(0.05)
    if value == 1:
        time.sleep(0.2)
    for i in gpio_list:
        gpio.output(i, gpio.LOW)

if __name__ == '__main__':
    go()
    gpio.cleanup()
