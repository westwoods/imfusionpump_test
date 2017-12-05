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
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# setup input switches
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(19, GPIO.IN)

GPIO.setup(26, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.IN)

def swc_callback(channel):
	time.sleep(0.02)
	if  GPIO.input(channel)==0:
		sw_module.play_click()
		if channel == 19:
			digit = 1
			if (sw_module.value%(digit*10))/digit <9:
				sw_module.value += digit
			elif (sw_module.value%(digit*10))/digit == 9:
				sw_module.value -= digit*9
		if channel == 21:
			digit =10
			if (sw_module.value%(digit*10))/digit <9:
				sw_module.value += digit
				
			elif (sw_module.value%(digit*10))/digit == 9:
				sw_module.value -= digit*9== 20:
			digit =100
			print((sw_module.value%(digit*10))/digit)
			if (sw_module.value%(digit*10))/digit <9:
				sw_module.value += digit
			elif (sw_module.value%(digit*10))/digit == 9:
				sw_module.value -= digit*9
		if channel == 5:
			digit =1000
			if (sw_module.value%(digit*10))/digit <9:
				sw_module.value += digit
			elif (sw_module.value%(digit*10))/digit == 9:
				sw_module.value -= digit*9
		if channel == 26:
			digit = 1
			if (sw_module.value%(digit*10))/digit >0:
				sw_module.value -= digit
			elif (sw_module.value%(digit*10))/digit == 0:
				sw_module.value += digit*9
		if channel == 16:
			digit = 10
			if (sw_module.value%(digit*10))/digit >0:
				sw_module.value -= digit
			elif (sw_module.value%(digit*10))/digit == 0:
				sw_module.value += digit*9
		if channel == 13:
			digit = 100
			if (sw_module.value%(digit*10))/digit >0:
				sw_module.value -= digit
			elif (sw_module.value%(digit*10))/digit == 0:
				sw_module.value += digit*9
		if channel == 6:
			digit = 1000
			if (sw_module.value%(digit*10))/digit >0:
				sw_module.value -= digit
			elif (sw_module.value%(digit*10))/digit == 0:
				sw_module.value += digit*9
		print(digit)

# setup gpio interrupts
GPIO.add_event_detect(5, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(6, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(13, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(19, GPIO.BOTH, callback=swc_callback,bouncetime=10)

GPIO.add_event_detect(26, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(16, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(20, GPIO.BOTH, callback=swc_callback,bouncetime=10)
GPIO.add_event_detect(21, GPIO.BOTH, callback=swc_callback,bouncetime=10)


print("start")
sw_module.loop_start(test_thing="D",sw_digit_mode = True)
