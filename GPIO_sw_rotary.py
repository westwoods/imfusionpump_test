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
rotary_input_q=[0,0,0,0,0]
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
			rotary_input_q[index]=direction
			index=(index+1)%5
			if sum(rotary_input_q) >0:
				delta=sum([abs(x) for  x in rotary_input_q])
			else:
				delta=-sum([abs(x) for  x in rotary_input_q])
			if direction !=0:
				if abs(delta)>=20:#빠른 회전
					print ("rotate:",delta)
					sw_module.update_val(delta*abs(delta)/2)
				elif abs(delta)>=5: #중간회전
					self.count[1]+=1
					print ("self.count",self.count)
					if self.count[1]>=4:
						self.count[1]=0
						sw_module.update_val(delta)
				else: #느린회전
					self.count[0]+=1
					print ("self.count",self.count)
					if self.count[0]>=4:
						self.count[0]=0
						sw_module.update_val(direction/abs(direction))
			time.sleep(0.01)
print("noew")
print("start")

controller=c_Controller()
controller.daemon =True
controller.start()
sw_module.loop_start(test_thing="R")
