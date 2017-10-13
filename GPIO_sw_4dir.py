#! /usr/bin/python3
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
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# setup input switches
GPIO.setup(21, GPIO.IN)
GPIO.setup(17, GPIO.IN)

GPIO.setup(5, GPIO.IN)

GPIO.setup(13, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# setup next switch


def up(channel):
    sw_module.value += sw_module.digit
    print("pushed up",sw_module.digit)
def down(channel):
    sw_module.value -= sw_module.digit
    print("pushed down",sw_module.digit)
def left(channel):
    if sw_module.digit < 1000:
        sw_module.digit *=10
    
def right(channel):
    global digit
    if sw_module.digit > 1:
        sw_module.digit = int(sw_module.digit/10)
        
# setup gpio interrupts
GPIO.add_event_detect(21, GPIO.RISING, callback=up,bouncetime=100)

GPIO.add_event_detect(22, GPIO.RISING, callback=down,bouncetime=100)

GPIO.add_event_detect(5, GPIO.RISING, callback=left,bouncetime=100)

GPIO.add_event_detect(13, GPIO.RISING, callback=right,bouncetime=100)

    

    
print("start")
sw_module.loop_start()
