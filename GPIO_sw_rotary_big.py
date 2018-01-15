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
qsize = 12
rotary_input_q = [0] * qsize
index=0


class c_Controller(threading.Thread):
	def __init__(self):
		super(c_Controller,self).__init__()
		A_PIN  = 21
		B_PIN  = 23
		SW_PIN = 22
		
		self.STOP = 0
		self.LOW = 1
		self.MID = 2
		self.HIGH = 3
		
		self.count=[0,0,0]
		self.gpio = gaugette.gpio.GPIO()
		self.encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(self.gpio,A_PIN, B_PIN)
		self.encoder.start()
		self.switch = gaugette.switch.Switch(self.gpio,SW_PIN)
		self.mode = self.STOP
	
	def signal_handler(self, signal, frame):
		print ('turn off')
		sys.exit(1)
	
	def decide_mode(self, rotary_input):
		level1 = 9000
		level2 = 29000
		
		if abs(sum(rotary_input_q)*100) <= level1/(math.log(sw_module.value+100)+2): #low speed
			self.mode = self.LOW
		elif abs(sum(rotary_input_q)*100) <= level2/(math.log(sw_module.value+100)+2): #mid speed
			self.mode = self.MID
		else:
			self.mode = self.HIGH
			
		return self.mode
		
	def run_input_mk0(self):
		global index
		
		level1 = 11000
		level2 = 21500
				
		count_0 = 0
		count_1 = 0
		count_2 = 0
		
		step_0 = 1
		step_1 = 8
		step_2 = 50
		
		captureValue = -1
		sumOfinputQ = 0
		
		while True :
			# get direction of encoder
			direction = self.encoder.get_steps()
						
			# decide mode

			###
			if direction != 0: #input rotary encoder
				# temporary store for unit increase
				if captureValue == -1:
					captureValue = sw_module.value
					
				speed = abs(sum(rotary_input_q) * 100)
				rotary_input_q[index] = direction
				
				# low speed
				if speed <= level1 / (math.log(sw_module.value + 100) + 2):
					count_0 += direction
					
					if abs(count_0) > 3:
						sw_module.update_val(count_0/abs(count_0))
						print(0, ':', abs(sum(rotary_input_q)))
						count_0 = 0
				# mid speed
				elif speed <= level2 / (math.log(sw_module.value + 100) + 2):
					count_1 += direction
					
					# round decimal 
					if direction > 0:
						sw_module.update_val(10 - (sw_module.value % 10 ))
					else:
						sw_module.update_val(- (sw_module.value % 10 ))
					
					if abs(count_1) > 2:
						#print("module value:", sw_module.value)
						sw_module.update_val(count_1/abs(count_1) * step_1)
						count_1 = 0
						print(1, ':', abs(sum(rotary_input_q)))
				else: #high speed
					count_2 += direction
					
					# round decimal
					if direction > 0:
						sw_module.update_val(10 - (sw_module.value % 10 ))
					else:
						sw_module.update_val(- (sw_module.value % 10 ))
					
					if abs(count_2) > 2:
						sw_module.update_val(count_2/abs(count_2) * step_2)
						count_2 = 0
						print(2, ':', abs(sum(rotary_input_q)))
						
				sumOfinputQ = sumOfinputQ + sum(rotary_input_q) #integral 
			else:
				# unit increase threshold
				if abs(sumOfinputQ) > 30 and abs(sumOfinputQ) < 200:
					sw_module.value = captureValue + int(sumOfinputQ/abs(sumOfinputQ)*10)
					
					if sumOfinputQ > 0:
						sw_module.update_val(- (sw_module.value % 10))
					else:
						sw_module.update_val(10 - (sw_module.value % 10) if sw_module.value % 10 != 0 else 0)

					#print(3,abs(sum(rotary_input_q))*100,level1/(math.log(sw_module.value+1)+1),"*"*abs(sum(rotary_input_q)))
				#print(sumOfinputQ)
						
			    # reset variables
				if index == 0:
					captureValue = -1
					sumOfinputQ = 0
				
				rotary_input_q[index]=0
			
			# increase index (0...9)
			index = (index + 1) % 10
			time.sleep(0.01)
			
	def run_input_mk1(self):
		global index
		
		level1 = 8000
		level2 = 15000
		level3 = 18000
		level4 = 21000
				
		count = 0
		
		step_0 = 1
		step_1 = 1
		step_2 = 5
		step_3 = 15
		step_4 = 50
		
		captureValue = -1
		sumOfinputQ = 0
		
		while True :
			# get direction of encoder
			direction = self.encoder.get_steps()
						
			# decide mode

			###
			if direction != 0: #input rotary encoder
				
				# temporary storage for unit increase
				if captureValue == -1:
					captureValue = sw_module.value
					
				speed = abs(sum(rotary_input_q)/len(rotary_input_q) * 1000)
				rotary_input_q[index] = direction
				count += direction
				
				sumOfinputQ += sum(rotary_input_q)/len(rotary_input_q) * 10 #integral 
				
				# decimal speed
				if speed <= level1 / (math.log(sw_module.value + 100) + 2):
					
					if abs(count) > 3:
						incr = count/abs(count)
						sw_module.update_val(incr)
						count = 0
						
						print(0, ':', abs(sum(rotary_input_q)),':', incr, ':', sw_module.value)
				# step 1
				elif speed <= level2 / (math.log(sw_module.value + 100) + 2):
					if abs(count) > 2:
						incr = count/abs(count) * step_1
					
						sw_module.update_val(incr)
						count = 0
						
						# round decimal 
						if direction > 0:
							sw_module.update_val(10 - (sw_module.value % 10 ))
						else:
							sw_module.update_val(- (sw_module.value % 10 ))
						
						print(1, ':', abs(sum(rotary_input_q)),':', incr, ':', sw_module.value)
				# step 2
				elif speed <= level3 / (math.log(sw_module.value + 100) + 2): 
					if abs(count) > 2:
						incr = count/abs(count) * step_2
						#incr = count * step_2

						sw_module.update_val(incr)
						count = 0
						
						# round decimal
						if direction > 0:
							sw_module.update_val(10 - (sw_module.value % 10 ))
						else:
							sw_module.update_val(- (sw_module.value % 10 ))
						
						print(2, ':', abs(sum(rotary_input_q)),':', incr, ':', sw_module.value)
				# step 3
				elif speed <= level4 / (math.log(sw_module.value + 100) + 2): 
					if abs(count) > 2:
						incr = count/abs(count) * step_3

						sw_module.update_val(incr)
						count = 0
						
						# round decimal
						if direction > 0:
							sw_module.update_val(10 - (sw_module.value % 10 ))
						else:
							sw_module.update_val(- (sw_module.value % 10 ))
						
						print(3, ':', abs(sum(rotary_input_q)),':', incr, ':', sw_module.value)
				# step 4
				else: 
					if abs(count) > 2:
						incr = count/abs(count) * step_4

						sw_module.update_val(incr)
						count = 0
						
						# round decimal
						if direction > 0:
							sw_module.update_val(10 - (sw_module.value % 10 ))
						else:
							sw_module.update_val(- (sw_module.value % 10 ))

						print(4, ':', abs(sum(rotary_input_q)),':', incr, ':', sw_module.value)
			else:
				# unit increase threshold
				if abs(sumOfinputQ) > 28 and abs(sumOfinputQ) < 200:
					sw_module.value = captureValue + int(sumOfinputQ/abs(sumOfinputQ)*10)
					
					if sumOfinputQ > 0:
						sw_module.update_val(- (sw_module.value % 10))
					else:
						sw_module.update_val(10 - (sw_module.value % 10) if sw_module.value % 10 != 0 else 0)

					#print(3,abs(sum(rotary_input_q))*100,level1/(math.log(sw_module.value+1)+1),"*"*abs(sum(rotary_input_q)))
				#print(sumOfinputQ)
						
			    # reset variables
				if index == 0:
					captureValue = -1
					sumOfinputQ = 0.0
				
				rotary_input_q[index]=0
			
			# increase index (0...qsize - 1)
			index = (index + 1) % qsize
			time.sleep(0.01)
	
	def run_input(self):
		global index

		count = 0
		count10 = 0
		count100 = 0
		captureValue = -1
		sumOfinputQ = 0
		level1 = 9000
		level2 = 21000
		
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
			###
			if direction !=0: #input rotary encoder
				if captureValue == -1:
					captureValue = sw_module.value
				if abs(sum(rotary_input_q)*100) <= level1/(math.log(sw_module.value+100)+2): #low speed
					rotary_input_q[index]= direction
					count = count + direction
					if abs(count) > 3:
						sw_module.update_val(count/abs(count))
						print(1,abs(sum(rotary_input_q)))
						count = 0
				elif direction !=0 and abs(sum(rotary_input_q)*100) >level1/(math.log(sw_module.value+100)+2) and abs(sum(rotary_input_q)*100) <=level2/(math.log(sw_module.value+100)+2): #mid speed
					rotary_input_q[index]= direction 
					count10 = count10 + direction
					if abs(count10) > 2:
						sw_module.update_val(count10/abs(count10)*10)
						count10 = 0
						print(2,abs(sum(rotary_input_q)))
				elif direction !=0: #high speed
					rotary_input_q[index]= direction
					count100 = count100 + direction
					if abs(count100) > 2:
						sw_module.update_val(count100/abs(count100)*100)
						count100 = 0
						print(3,abs(sum(rotary_input_q)))
				sumOfinputQ = sumOfinputQ + sum(rotary_input_q) #integral 
			else:
				
				if abs(sumOfinputQ) > 20 and abs(sumOfinputQ) < 200:
					sw_module.value = captureValue+ int(sumOfinputQ/abs(sumOfinputQ)*10)
					#print(3,abs(sum(rotary_input_q))*100,level1/(math.log(sw_module.value+1)+1),"*"*abs(sum(rotary_input_q)))
				#print(sumOfinputQ)
				if index == 0:
					captureValue = -1
					sumOfinputQ = 0
				rotary_input_q[index]=0
			index=(index+1)%10
			time.sleep(0.01)
	
	def run(self):
		#self.run_input()
		self.run_input_mk1()
	

print("Rotary: start")

controller=c_Controller()
controller.daemon =True
controller.start()
sw_module.loop_start(test_thing="R",smallbig = "big", sw_rotary_mode = True)
