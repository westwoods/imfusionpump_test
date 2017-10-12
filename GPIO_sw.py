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
    
def init_hardware():
    
    GPIO.setmode(GPIO.BCM)
  
    # setup input switches
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(14, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.IN)
    
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.IN)
    
    # setup gpio interrupts
    # next button
    GPIO.add_event_detect(14, GPIO.RISING, callback=up1000back,bouncetime=100)
    GPIO.add_event_detect(15, GPIO.RISING, callback=up100back,bouncetime=100)
    GPIO.add_event_detect(16, GPIO.RISING, callback=up10back,bouncetime=100)
    GPIO.add_event_detect(12, GPIO.RISING, callback=up1back,bouncetime=100)
    
    GPIO.add_event_detect(22, GPIO.RISING, callback=dn1000back,bouncetime=100)
    GPIO.add_event_detect(23, GPIO.RISING, callback=dn100back,bouncetime=100)
    GPIO.add_event_detect(24, GPIO.RISING, callback=dn10back,bouncetime=100)
    GPIO.add_event_detect(25, GPIO.RISING, callback=dn1back,bouncetime=100)
    
    # initiaize lcd
    lcd = ST7032I2C.ST7032I(0x3e, 1)
    lcd.clear()

    return lcd

def up1back(channel):
    digit = 1
    if (sw_module.value%(digit*10))/10 <9:
        sw_module.value += digit
    
def up10back(channel):
    digit =10
    if (sw_module.value%(digit*10))/10 <9:
        sw_module.value += digit
        
def up100back(channel):
    digit =100
    if (sw_module.value%(digit*10))/10 <9:
        sw_module.value += digit
    
def up1000back(channel):
    digit =1000
    if (sw_module.value%(digit*10))/10 <9:
        sw_module.value += digit
        
def dn1back(channel):
    digit = 1
    if (sw_module.value%(digit*10))/10 >0:
        sw_module.value -= digit
    
def dn10back(channel):
    digit = 10
    if (sw_module.value%(digit*10))/10 >0:
        sw_module.value -= digit
def dn100back(channel):
    digit = 100
    if (sw_module.value%(digit*10))/10 >0:
        sw_module.value -= digit
    
def dn1000back(channel):
    digit = 1000
    if (sw_module.value%(digit*10))/10 >0:
        sw_module.value -= digit
print("start")
sw_module.loop_start()
