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
#import m_Controller.rotary_encoder as Rotary
rotary_input_q=[0,0,0,0,0,0,0,0,0,0,0,0,]
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
		count = 0
		count10 = 0
		count100 = 0
		last_state= 0
		while True :
			direction = self.encoder.get_steps()
			state= self.switch.get_state()
			if state!= last_state: #한번클릭시 메뉴가 여러번 넘어가지 않도록
				print ("switch %d" %state)
				last_state=state
				print("in run")
				if last_state==1:
					print('pushed')
			#delta = self.encoder.get_delta()
			if abs(direction) == 1:
				rotary_input_q[index]= direction
				count = count + direction
				if abs(count) > 3:
					sw_module.update_val(count/4)
					count = 0
			elif direction !=0 and abs(sum(rotary_input_q)) <=5:
				rotary_input_q[index]= direction
				sw_module.update_val(direction/2)
			elif direction !=0 and abs(sum(rotary_input_q)) >5 and abs(sum(rotary_input_q)) <=10:
				rotary_input_q[index]= direction
				count10 = count10 + direction
				if abs(count10) > 5:
					sw_module.update_val(count10/abs(count10)*10)
					count10 = 0
			elif direction !=0:
				rotary_input_q[index]= direction
				count100 = count100 + direction
				if abs(count100) > 10:
					sw_module.update_val(count100/abs(count100)*100)
					count100 = 0
			else:
				rotary_input_q[index]=0
			index=(index+1)%5
			time.sleep(0.01)
print("noew")
print("start")

controller=c_Controller()
controller.daemon =True
controller.start()
sw_module.loop_start(test_thing="R")
