#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author     Version      Date        Comments
# FQuinto    1.0.0        2015-Nov    First version fron NoConName 2015 event

# Do test
# Copyright (C) 2015 Fran Quinto

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import threading
import time, datetime
import json
import calendar
import os
import urllib, urllib2
import RPi.GPIO as GPIO
import Adafruit_DHT


GPIO.setwarnings(False)  # Turn off warnings
GPIO.setmode(GPIO.BOARD) # Config as BOARD

rel1_sirena = 35     # pin Relay 1 (board izquierda), GPIO 19
rel2_giro = 36   	 # pin Relay 2 (board izquierda), GPIO 16
rel3_luz_sirena = 37 # pin Relay 1 (board derecha),   GPIO 26

# setup all the pins
GPIO.setup(rel1_sirena, GPIO.OUT)
GPIO.setup(rel2_giro, GPIO.OUT)
GPIO.setup(rel3_luz_sirena, GPIO.OUT)

# INIT
GPIO.output(rel1_sirena, 1)  #Turn OFF
GPIO.output(rel2_giro, 1)  #Turn OFF
GPIO.output(rel3_luz_sirena, 1)  #Turn OFF

sensor = Adafruit_DHT.DHT22
# Pins
temphum = 2 # GPIO2, pin 3

# USUARIOS CONFIGURATION
nombre1 = 'Fran'
blink1_id1 = '0011xxxxxxxxxx23' # CHANGE THIS!
ifttt_key1 = 'insert_here_key_from_IFTTT' # CHANGE THIS!

# pasa el now a valor del blink
last_time = int(datetime.datetime.now().strftime("%s"))

class ordenesWeb (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		# A flag to notify the thread that it should finish up and exit
		self.kill_received = threading.Event()
	def run(self):
		while not self.kill_received.is_set():
			# print ("Starting " + self.name)
			global blink1_id1
			global last_time
			global nombre1
			self.leeweb(blink1_id1,last_time,nombre1)
			last_time = calendar.timegm(time.gmtime())
			time.sleep(5)
			# print ("Exiting " + self.name)
	def leeweb(self, blink_id, last_time, nombre):

		global blink1_id1
		global ifttt_key1

		now = time.strftime("%a, %d %b %Y %H:%M")

		url = 'http://api.thingm.com/blink1/events/'+blink_id
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)
		data = res.read()

		ev = json.loads(data)

		if ev['event_count'] > 0:
			#print ('events to process')
			for e in ev['events']:
				#print (e)
				if int(e['date']) > last_time:
					if e['name'] == 'GIRO_ON':
						# Set GIRO_ON
						GPIO.output(rel2_giro, 0)  #Turn ON
						message = nombre + ' ha activado el GIRO'
						print message
						# data = urllib.urlencode({'value1' : now, 'value2' : message})
						# url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						# content = urllib2.urlopen(url=url, data=data).read()
					if e['name'] == 'GIRO_OFF':
						# Set GIRO_OFF
						GPIO.output(rel2_giro, 1)  #Turn OFF
						message = nombre + ' ha desactivado el GIRO'
						print message
						# data = urllib.urlencode({'value1' : now, 'value2' : message})
						# url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						# content = urllib2.urlopen(url=url, data=data).read()
					if e['name'] == 'LUZ_ON':
						# Set LUZ_ON
						GPIO.output(rel3_luz_sirena, 0)  #Turn ON
						message = nombre + ' ha activado la luz'
						print message
						# data = urllib.urlencode({'value1' : now, 'value2' : message})
						# url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						# content = urllib2.urlopen(url=url, data=data).read()
					if e['name'] == 'LUZ_OFF':
						# Set LUZ_OFF
						GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
						message = nombre + ' ha desactivado la luz'
						print message
						# data = urllib.urlencode({'value1' : now, 'value2' : message})
						# url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						# content = urllib2.urlopen(url=url, data=data).read()
					if e['name'] == 'ASUSTAR':
						# Set ASUSTAR
						GPIO.output(rel3_luz_sirena, 0)  #Turn ON
						os.system('mpg321 -g 100 -q mob_ua-gun_shoot_m_16.mp3 &')
						time.sleep(1)
						GPIO.output(rel2_giro, 0)  #Turn ON
						time.sleep(0.75)
						GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
						time.sleep(0.75)
						GPIO.output(rel3_luz_sirena, 0)  #Turn ON
						#GPIO.output(rel1_sirena, 0)  #Turn ON
						time.sleep(0.75)
						GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
						time.sleep(0.75)
						#GPIO.output(rel1_sirena, 1)  #Turn OFF
						GPIO.output(rel3_luz_sirena, 0)  #Turn ON
						time.sleep(0.75)
						GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
						time.sleep(0.75)
						GPIO.output(rel3_luz_sirena, 0)  #Turn ON
						time.sleep(1.5)
						GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
						GPIO.output(rel2_giro, 1)  #Turn OFF
						message = nombre + ' ha asustado'
						print message
						# data = urllib.urlencode({'value1' : now, 'value2' : message})
						# url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						# content = urllib2.urlopen(url=url, data=data).read()
					if e['name'] == 'dimeTEMP2':
						# Set dimeTEMP2
						humidity, temperature = Adafruit_DHT.read_retry(sensor, temphum)
						if humidity is not None and temperature is not None:
							message = 'temperature:{0:0.1f},humidity:{1:0.1f}'.format(temperature, humidity)
						else:
							message = 'temperature:0,humidity:0'
						print message
						data = urllib.urlencode({'value1' : now, 'value2' : message})
						url = 'https://maker.ifttt.com/trigger/Mensaje/with/key/'+str(ifttt_key1)+'/'
						content = urllib2.urlopen(url=url, data=data).read()
		return


# Create new threads
thread1 = ordenesWeb(1, "Thread-1")

# Start new Threads
thread1.start()

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	# print ("attempting to close threads.")
	thread1.kill_received.set()

	GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
	GPIO.output(rel1_sirena, 1)  #Turn OFF
	GPIO.output(rel2_giro, 1)  #Turn OFF
	GPIO.cleanup()
	# print ("threads successfully closed")

# print ("Exiting Main Thread")

