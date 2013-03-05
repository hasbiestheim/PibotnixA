#!/usr/bin/env python

# Atom Bot 2 Server
# September 27, 2011
# Robert Svec
#
# Thanks to maSnun for the battery percentage script:
# http://www.masnun.me/2010/09/01/python-script-to-monitor-laptop-battery-charge-ubuntulinux-mint.html

import serial
import socket
import threading
import time
import Queue
import os
import commands

##########################################################
class checksensor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop = threading.Event()
	def run(self):
		while(killt == 0):
			mydata = str(sensor.read())
			response_queue.put(mydata)
			sensor.flush()
			sensor.flushInput()
			sensor.flushOutput()
			mydata = ""
#############################################################
class play(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop = threading.Event()
	def run(self):
		while(killt == 0):
			#os.system("omxplayer greenday.mp3")

response_queue = Queue.Queue()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9000))
sock.listen(1)
print "Listening on TCP 9000"
motor = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print "Connected to Motor Controller: /dev/ttyUSB0"
#os.system("omxplayer operational.mp3")

while(1):
	try:
		print "Waiting For Connection..."
		connection, addr = sock.accept()
		connection.setblocking(0)
		print "Connected by", addr[0]
		while(1):
			try:
				sockdata = connection.recv(1)
				break
			except:
				pass
		if (sockdata == 'V'):
			#os.system("omxplayer mostreliable.mp3")
			connection.close()
		if (sockdata == 'G'):
			#os.system("omxplayer greenday.mp3")
			connection.close()
		if (sockdata == 'C'):
			#os.system("omxplayer well.mp3")
			connection.close()
		if (sockdata == 'Q'):
			#os.system("omxplayer goodbye.mp3")
			connection.close()
		if (sockdata == 'M'):
			print "Entering Manual Mode"
			#os.system("omxplayer ignition.mp3")
			motor.write(sockdata)
			while(sockdata != 'X'):
				sockdata = '9'
				try:
					sockdata = connection.recv(1)
				except:
					pass
				if sockdata == 'X':
					break
				if sockdata == '0':
					motor.write(sockdata)
				if sockdata == '1':
					motor.write(sockdata)
				if sockdata == '2':
					motor.write(sockdata)
				if sockdata == '3':
					motor.write(sockdata)
				if sockdata == '4':
					motor.write(sockdata)
				if sockdata == '5':
					motor.write(sockdata)
				if sockdata == '6':
					motor.write(sockdata)
				else:
					pass
			motor.write('0')
			connection.close()
			print addr[0], "Closed Manual Mode"
			#os.system("omxplayer completed.mp3")
	except KeyboardInterrupt:
		print "Closing Server"
		connection.close()
		sock.close()
		motor.write('0')
		#os.system("omxplayer whatdouthinkurdoing.mp3")
		quit()
