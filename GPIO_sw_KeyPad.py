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
from pygame.locals import *

import RPi.GPIO as GPIO
import time
import ST7032I2C
from pad4pi import rpi_gpio

KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"],
    ]
ROW_PINS = [5,6,13,19] # 2,7,6,4 
COL_PINS = [26,20,21] #3,1,5
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS,col_pins=COL_PINS)
def printKey(key):
    print(key)
keypad.registerKeyPressHandler(printKey)
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
    GPIO.setup(14, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(17, GPIO.IN)

    GPIO.setup(22, GPIO.IN)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.IN)

    # setup next switch


    # initiaize lcd
    lcd = ST7032I2C.ST7032I(0x3e, 1)
    lcd.clear()

    return lcd


def process_GPIO(value):
    if GPIO.input(14) == 0:
        value += 100
    if GPIO.input(15) == 0:
        value += 10
    if GPIO.input(16) == 0:
        value += 1
    if GPIO.input(17) == 0:
        value += .1

    if GPIO.input(22) == 0:
        value -= 100
    if GPIO.input(23) == 0:
        value -= 10
    if GPIO.input(24) == 0:
        value -= 1
    if GPIO.input(25) == 0:
        value -= .1

    return value

def input_number(num):
    # display the given number
    screen = pygame.display.get_surface()

    clock = pygame.time.Clock()
    print("before render", clock.get_time())

    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render(str(num), True, (255, 0, 0), (255, 255, 255))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
     
    screen.fill((255, 255, 255))
    screen.blit(text, textrect)
     
    pygame.display.update()
    clock.tick()
    print("after render", clock.get_time())
       
    # receive input from GPIO

    # check the time passed

    # check the value of input





if __name__ == '__main__':
    value = 0.0
    display = init_hardware()
    
    init_monitor()

    input_number(34)    

try: 
    while True:   
        value = process_GPIO(value)

        if value < 0.0:
            value = 0.0

        sval = "Value: {:05}".format(value)
        print(sval)

        display.addstr(sval, 0)


        time.sleep(.1)

except KeyboardInterrupt:
    GPIO.cleanup()

