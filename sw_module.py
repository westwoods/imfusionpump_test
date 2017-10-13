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

import pygame
import random
from pygame.locals import *

import RPi.GPIO as GPIO
import time
import ST7032I2C
import timeit
import pad4pi

def toggle_fullscreen():
	screen = pygame.display.get_surface()
	tmp = screen.convert()
	caption = pygame.display.get_caption()
	cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
	
	w,h = screen.get_width(),screen.get_height()
	flags = screen.get_flags()
	bits = screen.get_bitsize()
	
	pygame.display.quit()
	pygame.display.init()
	
	screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
	screen.blit(tmp,(0,0))
	pygame.display.set_caption(*caption)

	pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

	pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
	
	return screen

def init_monitor(SW = 1024, SH = 768):
	pygame.init()
	screen = pygame.display.set_mode((SW,SH))

	pygame.display.set_caption('Number Input Experiment')
	screen.fill((0,0,0))
	
	
def init_hardware(next_button_pin=17):
	GPIO.setmode(GPIO.BCM)
	# setup input switches
	GPIO.setup(next_button_pin, GPIO.IN)
	print("next_button pin=",next_button_pin)
	# setup next switch
	# setup gpio interrupts
	# next button
	GPIO.add_event_detect(next_button_pin, GPIO.RISING, callback=next,bouncetime=300)
	# initiaize lcd
	lcd = ST7032I2C.ST7032I(0x3e, 1)
	lcd.clear()

	return lcd


def next(channel):
	print("next button pushed")
	global index, input_list, a,value,start, end_flag, end,time_list,input_list
	if index<len(testNum_list)-1:
		index += 1
	else:
		end_flag = True
	end = timeit.default_timer()
	time_list.append(end - start)
	input_list.append(value)
	print("runtime", end - start,end_flag,index,"  ",len(testNum_list))
	start = timeit.default_timer()
	a = 100
	value = 0
	
def input_number(num=34):
	# display the given number
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	basicfont = pygame.font.SysFont(None, 48)
	print('{:.10}'.format(float(num)/10))
	text = basicfont.render('{:.10}'.format(float(num)/10), True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery
	screen.blit(text, textrect)
	clock.tick()
	
def print_screen(str="THANK YOU"):
	# display the given number
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	#print("before render", clock.get_time())
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render(str, True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery
	screen.blit(text, textrect)
	clock.tick()
	
def timer(num,togle=True):
	# display the given number
	screen = pygame.display.get_surface()
	
	basicfont = pygame.font.SysFont(None, 48)
	text = basicfont.render("timer :"+str(num), True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx + 250
	textrect.centery = screen.get_rect().centery + 250
	if togle:
		screen.blit(text, textrect)


def update_val(delta = 0):
	global value
	value+=int(delta)
	if value < 0:
		value = 0
	if value > 9999:
		value = 9999
	print("value:",value)

end_flag = False
f = open('input.txt', 'r')
testNum_list = []
input_list = []
time_list = []
for line in f:
	print(line)
	testNum_list.append(int(line))
	random_index=random.sample(range(len(testNum_list)), len(testNum_list)) #random without duplicates
value = 0
display = init_hardware()
index = 0
init_monitor()
start = timeit.default_timer()
digit = 10
a=1000
togle = 0
def loop_start(digit_cursor = False):
	global digit,value,f,time_list,end_flag,a,togle,index
	fw = open('output.txt', 'w')
	try:
		while not end_flag:
			a-=1
			togle+=1
		   # value = process_GPIO(value)
			#pygame.display.flip() #지우는??
			screen = pygame.display.get_surface()
			screen.fill((0,0,0))
			if a < 0:
				a = 0
			input_number(testNum_list[random_index[index]])
			if a==0:
				timer(a/10,togle%30>15)
			else:
				timer(a/10,True)
			pygame.display.update()
			if value < 0:
				value = 0
			
			sval = "Value: {:3}".format(int(value/10))
			if digit==1 or (value%10 != 0):
				sval = sval+"."+str( value%10)
			if togle%30>15 or digit_cursor:
				sval ='_' +sval[1:]
			sval =sval+"           "#인트 타입으로 바꾸고 마지막 자리에 소숫점가 추가
			
			display.addstr(sval, 0)
			time.sleep(.01)
		screen = pygame.display.get_surface()
		screen.fill((0,0,0))
		print_screen()
		pygame.display.update()
		display.addstr("THANK YOU      ", 0)
		fw.write("[order] [testNum] [inputNum] [time]\n")
		for order in range(len(random_index)):
			reorder_index=random_index.index(order)
			print("reorder_index",reorder_index)
			data = "{:0>4}    {:0>4}      {:0>4}       {:>.3} \n".format(order,testNum_list[order],input_list[reorder_index],time_list[reorder_index])
			fw.write(data)
		f.close()
		fw.close()
	except KeyboardInterrupt:
		f.close()
		fw.close()
		GPIO.cleanup()


