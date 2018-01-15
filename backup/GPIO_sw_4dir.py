#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# P14  UP 100
# P15  UP 10
# P16  UP 1
# P17  UP .1

# P22   DN 100
# P23   DN 10
# P24   DN 1
# P25   DN .1
import sw_module
#GPIO.setmode(GPIO.BCM)

# setup input switches
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)

GPIO.setup(13,GPIO.IN)

GPIO.setup(19,GPIO.IN)
# setup next switch


def swc_callback(channel):
    time.sleep(0.002)
    if  GPIO.input(channel)==0:
        sw_module.play_click()
        if channel == 6:
            if (sw_module.value%(sw_module.digit*10))/sw_module.digit <9:
                sw_module.value += sw_module.digit
            elif (sw_module.value%(sw_module.digit*10))/sw_module.digit == 9:
                sw_module.value -= sw_module.digit*9
            print("pushed up",sw_module.digit)
        if channel == 19:
            if (sw_module.value%(sw_module.digit*10))/sw_module.digit >0:
                sw_module.value -= sw_module.digit
            elif (sw_module.value%(sw_module.digit*10))/sw_module.digit == 0:
                sw_module.value += sw_module.digit*9
            print("pushed down",sw_module.digit)
        if channel == 13:
            if sw_module.digit<1000:
                sw_module.digit *=10
        if channel == 5:
            if sw_module.digit>1:
                sw_module.digit = int(sw_module.digit/10)

# setup gpio interrupts
GPIO.add_event_detect(6, GPIO.BOTH, callback=swc_callback,bouncetime=80)

GPIO.add_event_detect(19, GPIO.BOTH, callback=swc_callback,bouncetime=80)

GPIO.add_event_detect(13, GPIO.BOTH, callback=swc_callback,bouncetime=80)

GPIO.add_event_detect(5, GPIO.BOTH, callback=swc_callback,bouncetime=80)

print("start")
sw_module.loop_start(test_thing="F",sw_4dir_mode=True)
