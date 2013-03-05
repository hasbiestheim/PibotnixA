#!/usr/bin/env python

################################################################
# Module:   multijoystick.py
# Created:  2 April 2008
# Author:   Brian D. Wendt
#   http://principialabs.com/
# Version:  0.2
# License:  GPLv3
#   http://www.fsf.org/licensing/
'''
Provides four-axis joystick servo control from a PC
using the Arduino "MultipleServos" sketch
and the Python "servo.py" serial abstraction module.

Parts of this code were adapted from:
  http://svn.lee.org/swarm/trunk/mothernode/python/multijoy.py

NOTE: This script requires the following Python modules:
  pyserial - http://pyserial.sourceforge.net/
  pygame   - http://www.pygame.org/
  servo    - http://principialabs.com/
 Win32 users may also need:
  pywin32  - http://sourceforge.net/projects/pywin32/
'''
################################################################

import pygame
import socket
import time

def smove(servo, angle):
    if (0 <= angle <= 180):
	if (int(servo) == 1) and (int(angle) < 90):
		sock.send('2')

	if (int(servo) == 1) and (int(angle) > 90):
		sock.send('3')

	if (int(servo) == 2) and (int(angle) < 90):
		sock.send('1')

	if (int(servo) == 2) and (int(angle) > 90):
		sock.send('4')

	if (int(servo) == 3) and (int(angle) < 90):
		sock.send('5')
	if (int(servo) == 3) and (int(angle) > 90):
		sock.send('6')

	if (int(servo) == 3) and (int(angle) == 90):
		sock.send('7')
	if (int(servo) == 0) and (int(angle) == 0):
		sock.send('0') 
    else:
        print "Servo angle must be between 0 and 180.\n"


# allow multiple joysticks
joy = []

# handle joystick event
def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"
        if (e.dict['axis'] == 1):
            axis = "Y"
        if (e.dict['axis'] == 2):
            axis = "Throttle"
        if (e.dict['axis'] == 3):
            axis = "Z"
        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # uncomment to debug
            #output(str, e.dict['joy'])
            if (axis == "X"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                serv = int(90 + move)
                # and send to Arduino
                smove(1, serv)
            # Arduino joystick-servo hack
            if (axis == "Y"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                serv = int(90 + move)
                # and send to Arduino
                smove(2, serv)
            # Arduino joystick-servo hack
            if (axis == "Z"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                serv = int(90 + move)
                # and send to Arduino
                smove(3, serv)
            # Arduino joystick-servo hack
            if (axis == "Throttle"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                serv = int(90 + move)
                # and send to Arduino
                smove(4, serv)
    elif e.type == pygame.JOYBUTTONDOWN:
        str = "Button: %d" % (e.dict['button'])
        # uncomment to debug
        #output(str, e.dict['joy'])
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 0):
	    	return False
	if (e.dict['button'] == 1):
	    	#print "Button 2"
		smove(0,0)		
	if (e.dict['button'] == 2):
	    	print "Button 3"
	if (e.dict['button'] == 3):
	    	print "Button 4"
	if (e.dict['button'] == 4):
	    	print "Button 5"
	if (e.dict['button'] == 5):
	    	print "Button 6"
    else:
        pass

# print the joystick position
def output(line, stick):
    print "Joystick: %d; %s" % (stick, line)

# wait for joystick input
def joystickControl():
    pausecount = 0
    while True:
	e = pygame.event.get()
	if (len(e) > 0):
		for curevent in e:
			if (curevent.type == pygame.JOYBUTTONDOWN):
				if (handleJoyEvent(curevent) == False):
					return
			if (curevent.type == pygame.JOYAXISMOTION):
				if (pausecount < 15):
					pausecount = pausecount + 1
				else:
					handleJoyEvent(curevent)
					pausecount = 0
			else:
				pass
	else:
		pass


##########################################################
#########		MAIN PROGRAM		##########
##########################################################
while(1):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("192.168.1.108", 9000))
	a = raw_input("CMD:")
	if (a == 'm'):
		sock.send('M')
		pygame.joystick.init()
		pygame.display.init()
		if not pygame.joystick.get_count():
			print "\nConnect Joystick\n"
			quit()
		for i in range(pygame.joystick.get_count()):
			myjoy = pygame.joystick.Joystick(i)
			myjoy.init()
			joy.append(myjoy)
		joystickControl()
		sock.send('X')
	if (a == 'g'):
		sock.send('G')
		print "Green Day!"
		sock.send('X')
		sock.close()
	if (a == 'v'):
		sock.send('V')
		print "HAL 9000"
		sock.send('X')
	if (a == 'c'):
		print "HAL 9000"
		sock.send('C')
		sock.close()
	if (a == 'q'):
		sock.send('Q')
		print "Goodbye"
		sock.close()
		quit()
	else:
		sock.close()

