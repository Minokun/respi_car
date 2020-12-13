from pca9685 import PCA9685
from evdev import InputDevice
from select import select
import time
from led import ledShark, ledLight
import threading
from run import go

pwm = PCA9685(0x40, debug=True)
pwm.setPWMFreq(50)

def setPwmAngle(channel, angle):
    if channel == 0:
        angle = int(angle / 270 * 2000) + 500
    else:
        angle = int(angle / 180 * 2000) + 500
    pwm.setServoPulse(channel, angle)

def control():
    angle_0 = 100
    angle_1 = 90
    diff = 20
    time_delay = 0.25
    setPwmAngle(0, angle_0)
    setPwmAngle(1, angle_1)
    time.sleep(0.5)
    dev = InputDevice('/dev/input/event0')
    while True:
        select([dev], [], [])
        for event in dev.read():
            if event.value == 1:
                #up 17 left 30 right 32 down 31
                #channel 0 270 channel 1 180
                if angle_0 < 0:
                    angle_0 = 0
                if angle_0 > 270:
                    angle_0 = 270
                if angle_1 < 0:
                    angle_1 = 0
                if angle_1 > 180:
                    angle_1 = 180
                if event.code == 32:
                    angle_0 -= diff
                    print('left:', angle_0)
                    setPwmAngle(0, angle_0)
                    time.sleep(time_delay)
                if event.code == 30:
                    angle_0 += diff
                    print('right:', angle_0)
                    setPwmAngle(0, angle_0)
                    time.sleep(time_delay)
                if event.code == 17:
                    angle_1 += diff
                    print('up:', angle_1)
                    setPwmAngle(1, angle_1)
                    time.sleep(time_delay)
                if event.code == 31:
                    angle_1 -= diff
                    print('down:', angle_1)
                    setPwmAngle(1, angle_1)
                    time.sleep(time_delay)
                if event.code == 16:
                    angle_0 = 100
                    angle_1 = 90
                    setPwmAngle(0, angle_0)
                    setPwmAngle(1, angle_1)
                    print('channel 0: 0, channel 1: 0')
                if event.code == 25:
                    angle_0 = 225
                    angle_1 = 180
                    setPwmAngle(0, angle_0)
                    setPwmAngle(1, angle_1)
                    print('channel 0: 225, channel 1:180')
                if event.code == 3:
                    diff = 20
                if event.code == 4:
                    diff = 30
                if event.code == 5:
                    diff = 45
                if event.code == 19:
                    ledLight(['red'])
                if event.code == 34:
                    ledLight(['green'])
                if event.code == 21:
                    ledLight(['yellow'])
                if event.code == 59:
                    ls = threading.Thread(target=ledShark)
                    ls.start()
                if event.code == 20:
                    ledLight([])
            if event.value in (1,2) and event.code in [103, 105, 106, 108]:
                if event.code == 103:
                    go('front', event.value)
                    ledLight(['green'])
                if event.code == 108:
                    go('back', event.value)
                    ledLight(['red'])
                if event.code == 105:
                    go('left', event.value)
                    ledLight(['yellow'])
                if event.code == 106:
                    go('right', event.value)
                    ledLight(['yellow'])

if __name__ == '__main__':
    control()
