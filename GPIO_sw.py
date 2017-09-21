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
    
    
def init_hardware():
    
    GPIO.setmode(GPIO.BCM)
  
    # setup input switches
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(14, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(17, GPIO.IN)

    GPIO.setup(22, GPIO.IN)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.IN)

    # setup next switch
    
    # setup gpio interrupts
    # next button
    GPIO.add_event_detect(12, GPIO.RISING, callback=next,bouncetime=100)
    #
    GPIO.add_event_detect(14, GPIO.RISING, callback=up1000back,bouncetime=100)
    GPIO.add_event_detect(15, GPIO.RISING, callback=up100back,bouncetime=100)
    GPIO.add_event_detect(16, GPIO.RISING, callback=up10back,bouncetime=100)
    GPIO.add_event_detect(17, GPIO.RISING, callback=up1back,bouncetime=100)
    
    GPIO.add_event_detect(22, GPIO.RISING, callback=dn1000back,bouncetime=100)
    GPIO.add_event_detect(23, GPIO.RISING, callback=dn100back,bouncetime=100)
    GPIO.add_event_detect(24, GPIO.RISING, callback=dn10back,bouncetime=100)
    GPIO.add_event_detect(25, GPIO.RISING, callback=dn1back,bouncetime=100)
    
    # initiaize lcd
    lcd = ST7032I2C.ST7032I(0x3e, 1)
    lcd.clear()

    return lcd


def next(channel):
    print("next button pushed")
<<<<<<< HEAD
    global index, start, end, a, value
    index += 1
=======
    global index, input_list, start, end_flag, end
    if index<len(input_list)-1:
        index += 1
    else:
        end_flag = True
>>>>>>> cd9a2ec31e934f64a85ff284a6c1a940a1626521
    
    end = timeit.default_timer()
    print("runtime", end - start)
    start = timeit.default_timer()
    a = 100
    value = 0
    
def up1back(channel):
    global value
    digit = 1
    if (value%(digit*10))/10 <9:
        value += digit
    
def up10back(channel):
    global value
    digit =10
    if (value%(digit*10))/10 <9:
        value += digit
        
def up100back(channel):
    global value
    digit =100
    if (value%(digit*10))/10 <9:
        value += digit
    
def up1000back(channel):
    global value
    digit =1000
    if (value%(digit*10))/10 <9:
        value += digit
        
def dn1back(channel):
    global value
    digit = 1
    if (value%(digit*10))/10 >0:
        value -= digit
    
def dn10back(channel):
    global value
    digit = 10
    if (value%(digit*10))/10 >0:
        value -= digit
def dn100back(channel):
    global value
    digit = 100
    if (value%(digit*10))/10 >0:
        value -= digit
    
def dn1000back(channel):
    global value
    digit = 1000
    if (value%(digit*10))/10 >0:
        value -= digit

'''
def process_GPIO(value):
    if GPIO.input(14) == 0:
        value += 1000
    if GPIO.input(15) == 0:
        value += 100
    if GPIO.input(16) == 0:
        value += 10
    if GPIO.input(17) == 0:
        value += 1

    if GPIO.input(22) == 0:
        value -= 1000
    if GPIO.input(23) == 0:
        value -= 100
    if GPIO.input(24) == 0:
        value -= 10
    if GPIO.input(25) == 0:
        value -= 1

    return value
'''
def input_number(num=34):
    # display the given number
    screen = pygame.display.get_surface()

    clock = pygame.time.Clock()
    #print("before render", clock.get_time())

    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render(str(num), True, (255, 0, 0), (255, 255, 255))
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
    #print("after render", clock.get_time())
       
    # receive input from GPIO

    # check the time passed

    # check the value of input





if __name__ == '__main__':
    end_flag = False
    f = open('input.txt', 'r')
    input_list = []
    for line in f:
        print(line)
        input_list.append(int(line))
    random_index=random.sample(range(len(input_list)), len(input_list)) #random without duplicates
    value = 0
    display = init_hardware()
    index = 0
    init_monitor()
    start = timeit.default_timer()

try:
    a=1000
    togle = 0
    while not end_flag:
        a-=1
        togle+=1
       # value = process_GPIO(value)
        #pygame.display.flip() #지우는??
        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        if a < 0:
            a = 0
        input_number(input_list[random_index[index]])
        if a==0:
            timer(a/10,togle%30>15)
        else:
            timer(a/10,True)
        pygame.display.update()
        if value < 0:
            value = 0

        sval = "Value: {:04}".format(value)
        sval = sval[:-1] + "." + sval[-1:] #인트 타입으로 바꾸고 마지막 자리에 소숫점가 추가
        #print(sval)
        
        display.addstr(sval, 0)
        

        time.sleep(.01)
    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    print_screen()
    pygame.display.update()
    display.addstr("THANK YOU", 0)

except KeyboardInterrupt:
    GPIO.cleanup()

