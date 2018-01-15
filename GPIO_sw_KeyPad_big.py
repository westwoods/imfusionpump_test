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

from pad4pi import rpi_gpio
import sw_module

KEYPAD = [
	[1,2,3],
	[4,5,6],
	[7,8,9],
	[".",0,"←"],
	]
ROW_PINS = [13,21,6,19] # 2,7,6,4 
COL_PINS = [20,5,26] #3,1,5
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS,col_pins=COL_PINS)
sw_module.digit = 10
def printKey(key):
	sw_module.play_click()
	if key == "←":
		if sw_module.digit == 1:
			sw_module.value=int(sw_module.value-sw_module.value%10)
		else:
			sw_module.value=int((sw_module.value-sw_module.value%100)/10)
		sw_module.digit = 10
	elif key == ".":
		sw_module.digit = 1
	else: #NUMBER INPUt
		if sw_module.value<1000 and sw_module.digit != 1:
			sw_module.value=int(sw_module.value*10+key*sw_module.digit)
		else:
			sw_module.value=int(sw_module.value-sw_module.value%(sw_module.digit*10)+sw_module.value%(sw_module.digit)+key*sw_module.digit)
		
keypad.registerKeyPressHandler(printKey)
sw_module.loop_start(test_thing="K",smallbig = "big")

