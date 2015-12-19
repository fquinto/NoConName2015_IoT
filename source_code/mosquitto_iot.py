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

import RPi.GPIO as GPIO
import time
import os
import sys
import paho.mqtt.client as mqtt
import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# Pins
temphum = 2 # GPIO2, pin 3

GPIO.setwarnings(False)  # Turn off warnings
GPIO.setmode(GPIO.BOARD) # Config as BOARD

# Pins
red = 12    		 # pin RGB LED, GPIO 18
green = 16  	     # pin RGB LED, GPIO 23
blue = 18   		 # pin RGB LED, GPIO 24
pir = 32    		 # pin PIR sensor, GPIO 12
boton = 7			 # pin boton fisico, GPIO 4
rel1_sirena = 35     # pin Relay 1 (board izquierda), GPIO 19
rel2_giro = 36   	 # pin Relay 2 (board izquierda), GPIO 16
rel3_luz_sirena = 37 # pin Relay 1 (board derecha),   GPIO 26
rel4 = 38            # pin Relay 2 (board derecha),   GPIO 20

# setup all the pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)
GPIO.setup(boton, GPIO.IN)
GPIO.setup(rel1_sirena, GPIO.OUT)
GPIO.setup(rel2_giro, GPIO.OUT)
GPIO.setup(rel3_luz_sirena, GPIO.OUT)
GPIO.setup(rel4, GPIO.OUT)

wait = 0.1

# INIT
GPIO.output(red, 0)  #Turn OFF LED
GPIO.output(green, 0)  #Turn OFF LED
GPIO.output(blue, 0)  #Turn OFF LED
GPIO.output(rel1_sirena, 1)  #Turn OFF
GPIO.output(rel2_giro, 1)  #Turn OFF
GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
GPIO.output(rel4, 1)  #Turn OFF

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("orden")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+"\nMensaje: "+str(msg.payload))
	if (msg.topic == 'orden'):
		if (msg.payload == 'temperatura'):
			humidity, temperature = Adafruit_DHT.read_retry(sensor, temphum)
			if temperature is not None:
				message = 'temperatura:{0:0.1f}'.format(temperature)
			else:
				message = 'temperatura:0'
			client.publish("temperatura", message)
		if (msg.payload == 'humedad'):
			humidity, temperature = Adafruit_DHT.read_retry(sensor, temphum)
			if humidity is not None:
				message = 'humedad:{0:0.1f}'.format(humidity)
			else:
				message = 'humedad:0'
			client.publish("humedad", message)
		if (msg.payload == 'giroON'):
			GPIO.output(rel2_giro, 0)  #Turn ON
		if (msg.payload == 'luzON'):
			GPIO.output(rel3_luz_sirena, 0)  #Turn ON
		if (msg.payload == 'sirenaON'):
			GPIO.output(rel1_sirena, 0)  #Turn ON
		if (msg.payload == 'giroOFF'):
			GPIO.output(rel2_giro, 1)  #Turn OFF
		if (msg.payload == 'luzOFF'):
			GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
		if (msg.payload == 'sirenaOFF'):
			GPIO.output(rel1_sirena, 1)  #Turn OFF
		if (msg.payload == 'dispara'):
			os.system('mpg321 -g 100 -q mob_ua-gun_shoot_m_16.mp3 &')

try:
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("localhost", 1883, 60)

	wait = 0.1
	envia_mensaje_boton = True
	envia_mensaje_PIR = False

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	#client.loop_forever()
	while True:
		client.loop()
		if ((GPIO.input(boton) == False) and (envia_mensaje_boton)):
			envia_mensaje_boton = False
			client.publish("boton", "ON")
		elif (GPIO.input(boton) == True):
			envia_mensaje_boton = True
		if ((GPIO.input(pir) == True) and (envia_mensaje_PIR)):
			envia_mensaje_PIR = False
			client.publish("PIR", "ON")
		elif (GPIO.input(pir) == False):
			envia_mensaje_PIR = True
		time.sleep(wait)

except KeyboardInterrupt:  
		pass


GPIO.output(red, 0)  #Turn OFF LED
GPIO.output(green, 0)  #Turn OFF LED
GPIO.output(blue, 0)  #Turn OFF LED
GPIO.output(rel1_sirena, 1)  #Turn OFF
GPIO.output(rel2_giro, 1)  #Turn OFF
GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
GPIO.output(rel4, 1)  #Turn OFF

#Tidy up and remaining connections.  
GPIO.cleanup()