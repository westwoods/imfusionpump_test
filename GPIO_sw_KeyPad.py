
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

from pad4pi import rpi_gpio
import sw_module
KEYPAD = [
	[1,2,3],
	[4,5,6],
	[7,8,9],
	[".",0,"←"],
	]
ROW_PINS = [5,6,13,19] # 2,7,6,4 
COL_PINS = [26,20,21] #3,1,5
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS,col_pins=COL_PINS)

def printKey(key):
	if key == "←":
		print("key pressed")
		if sw_module.digit ==1:
			sw_module.value=int(sw_module.value-int(sw_module.value%(sw_module.digit*10)/sw_module.digit)*sw_module.digit)
			if sw_module.digit<10000:
				sw_module.digit*=10
		else :
			sw_module.value=int((sw_module.value-(sw_module.value%100))/10)+sw_module.value%10
			if sw_module.digit>10:
				sw_module.digit/=10
	elif key == ".":
		sw_module.digit = 1
	else:
		if sw_module.digit == 1:
			sw_module.value=int(sw_module.value-int(sw_module.value%(sw_module.digit*10)/sw_module.digit)*sw_module.digit)+key
		else:
			if sw_module.value<1000:
				sw_module.value=sw_module.value*10+key*10
			if sw_module.digit<10000:
				sw_module.digit*=10
print("noew")
keypad.registerKeyPressHandler(printKey)
print("start")
sw_module.loop_start()
