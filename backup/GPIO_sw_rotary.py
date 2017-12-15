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
import gaugette.rotary_encoder
import gaugette.switch
import gaugette.gpio
import sw_module
import time
import threading
import math
#import m_Controller.rotary_encoder as Rotary
rotary_input_q=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
index=0


class c_Controller(threading.Thread):
	def __init__(self):
		super(c_Controller,self).__init__()
		A_PIN  = 21
		B_PIN  = 23
		SW_PIN = 22
		self.count=[0,0,0]
		self.gpio = gaugette.gpio.GPIO()
		self.encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(self.gpio,A_PIN, B_PIN)
		self.encoder.start()
		self.switch = gaugette.switch.Switch(self.gpio,SW_PIN)
	
	def signal_handler(self, signal, frame):
		print ('turn off')
	
		sys.exit(1)
		
	def run(self):
		global index
		capture = -1
		cnt = 0
		while True :
			direction = self.encoder.get_steps()
			#delta = self.encoder.get_delta()
			"""
			if abs(direction) == 1:
				rotary_input_q[index]= direction
				count = count + direction
				if abs(count) > 3:
					sw_module.update_val(count/4)
					count = 0
				if sum(rotary_input_q):
					print(0,abs(sum(rotary_input_q))*100,50000/(sw_module.value+1),"*"*abs(sum(rotary_input_q)))
			"""
			rotary_input_q[index]= direction
			if not all(v==0 for v in rotary_input_q):
				if capture == -1:
					capture = sw_module.value
				if direction !=0:
					cnt = cnt + 1
					delta = abs(capture-sw_module.value)
					if cnt > (math.log(delta+1)+2):
						cnt = 0
						if ( delta<10) or sw_module.value < 10:
							sw_module.update_val(direction/abs(direction))
						elif delta <100 or sw_module.value <100 :
							sw_module.update_val((-sw_module.value%10)+direction/abs(direction)*10)
						elif delta <1000 or sw_module.value <1000 :
							sw_module.update_val((-sw_module.value%100)+direction/abs(direction)*100)
						elif delta <10000 or sw_module.value <10000 :
							sw_module.update_val((-sw_module.value%1000)+direction/abs(direction)*1000)
						print((rotary_input_q), direction, capture,(math.log(delta+1)+1))
			else:
				print((rotary_input_q), direction, capture,sw_module.value)
				capture = -1
			index=(index+1)%30
			time.sleep(0.01)
print("noew")
print("start")

controller=c_Controller()
controller.daemon =True
controller.start()
sw_module.loop_start(test_thing="R")
