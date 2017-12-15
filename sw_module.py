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
import concurrent.futures
import math
pygame.mixer.init()

click= [pygame.mixer.Sound("/home/pi/imfusionpump_test/click_sound1.wav"),pygame.mixer.Sound("/home/pi/imfusionpump_test/click_sound2.wav"),pygame.mixer.Sound("/home/pi/imfusionpump_test/Ticking_Clock.wav")]
test_name = input("input test#")
test_name = "S"+test_name
start_flag = False
end_flag = False
f = open('/home/pi/imfusionpump_test/input.txt', 'r')
testNum_list = []
input_list = []
time_list = []
value = 0
index = 0
start = timeit.default_timer()
digit = 10
a=1000
togle = 0
	
def play_click(song_num=0):
	click[song_num].stop()
	print("async play")
	time = 150 if song_num == 0 else 300
	click[song_num].play()

def count_down(song_num=2):
	click[song_num].stop()
	print("async play")
	time = 15000
	click[song_num].play()

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
	screen = pygame.display.set_mode((SW,SH))#,FULLSCREEN)
	pygame.display.set_caption('Number Input Experiment')
	screen.fill((0,0,0))

init_monitor()

def next_func(channel):
	#count_down()
	if GPIO.input(channel)==0:
		play_click(1)
		global start,index, input_list, a,value, end_flag, end,time_list,input_list,start_flag,digit
		print("next button pushed")
		if  not start_flag:
			start_flag = True
		else:
			if index<len(testNum_list)-1:
				index += 1
			else:
				end_flag = True
			end = timeit.default_timer()
			time_list.append(end - start)
			input_list.append(value)
			print("runtime", end - start,end_flag,index,"  ",len(testNum_list))
		start = timeit.default_timer()
		a = 300
		digit = 10
		value = 0
def init_hardware(next_button_pin=17):
	GPIO.setmode(GPIO.BCM)
	# setup input switches
	GPIO.setup(next_button_pin, GPIO.IN)
	print("next_button pin=",next_button_pin)
	# setup next switch
	# setup gpio interrupts
	# next button
	GPIO.add_event_detect(next_button_pin, GPIO.FALLING, callback=next_func,bouncetime=300)
	# initiaize lcd
	lcd = ST7032I2C.ST7032I(0x3e, 1)
	lcd.clear()

	return lcd
display = init_hardware()


def input_number(num=34):
	# display the given number
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	basicfont = pygame.font.SysFont(None, 255)
	outnum = "{:3}".format(int(num/10)) # 5white space
	if digit==1 or (num%10 != 0):
		outnum = outnum+"."+str( num%10)
	text = basicfont.render(outnum, True, (255, 0, 0), (255, 255, 255))
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
	basicfont = pygame.font.SysFont(None, 60)
	text = basicfont.render(str, True, (255, 0, 0), (255, 255, 255))
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery
	screen.blit(text, textrect)
	clock.tick()
	pygame.display.update()
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
	#print("value:",value)

if test_name == "St":
	for line in range(0,10):
			print(line)
			testNum_list.append(random.randint(1,1999))
			print(testNum_list)
			random_index=random.sample(range(len(testNum_list)), len(testNum_list)) #random without duplicates
else:
	for line in f:
		print(line)
		testNum_list.append(int(float(line)*10))
		print(testNum_list)
		random_index=random.sample(range(len(testNum_list)), len(testNum_list)) #random without duplicates


def loop_start(test_thing = "",sw_4dir_mode = False, sw_digit_mode = False,sw_rotary_mode = False):
	global digit,value,f,time_list,end_flag,a,togle,index,start_flag,test_name
	now_time=time.localtime()
	now_time=time.strftime(" %H:%M:%S")
	if not test_name == "St":
		fw = open("/home/pi/Desktop/"+test_thing+"/"+test_thing+test_name+now_time, 'w')
	try:
		while not end_flag:
			if not start_flag:
				screen = pygame.display.get_surface()
				screen.fill((0,0,0))
				print_screen("Press Next Button, If you ready")
				display.addstr("PressNextButton", 0)
				time.sleep(.6)
			else:
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
				if sw_digit_mode:
					sval = "      {:05.1f}".format(value/10) # 5white space
					sval =sval+"           "#인트 타입으로 바꾸고 마지막 자리에 소숫점가 추가
					display.addstr(sval, 0)
				elif sw_4dir_mode:
					sval = "      {:05.1f}".format(value/10) # 5white space
					sval =sval+"           "#인트 타입으로 바꾸고 마지막 자리에 소숫점가 추가
					if togle%30>15 and sw_4dir_mode:
						cursor = int(math.log10(digit))
						cursor = -1 if cursor == 0 else cursor
						sval =sval[0:9-cursor]+'_' +sval[10-cursor]
					display.addstr(sval, 0)
				else:
					sval = "      {:3}".format(int(value/10)) # 5white space
					if digit==1 or (value%10 != 0) or sw_rotary_mode:
						sval = sval+"."+str( value%10)
					sval =sval+"           "#인트 타입으로 바꾸고 마지막 자리에 소숫점가 추가
					display.addstr(sval, 0)
				time.sleep(.001)
		screen = pygame.display.get_surface()
		screen.fill((0,0,0))
		print_screen()
		display.addstr("THANK YOU      ", 0)
		fw.write("[order] [testNum] [inputNum] [time]\n")
		for order in range(len(random_index)):
			reorder_index=random_index.index(order)
			print("reorder_index",reorder_index , "order", order,len(input_list), len(testNum_list))
			data = "{:0>4}    {:0>4}      {:0>4}       {:>.3} \n".format(order,testNum_list[order],input_list[reorder_index],time_list[reorder_index])
			fw.write(data)
			
		if not test_name == "St":
			fw.write( "sum:{:>.3f}\n".format(sum(time_list)))
			fw.close()
		f.close()
	except KeyboardInterrupt:
		f.close()
		fw.close()
		GPIO.cleanup()


