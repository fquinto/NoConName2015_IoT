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

GPIO.setwarnings(False)  # Turn off warnings
GPIO.setmode(GPIO.BOARD) # Config as BOARD

# Pins
red = 12    		 # pin RGB LED, GPIO 18
green = 16  	     # pin RGB LED, GPIO 23
blue = 18   		 # pin RGB LED, GPIO 24
pir = 32    		 # pin PIR sensor, GPIO 12
rel1_sirena = 35     # pin Relay 1 (board izquierda), GPIO 19
rel2_giro = 36   	 # pin Relay 2 (board izquierda), GPIO 16
rel3_luz_sirena = 37 # pin Relay 1 (board derecha),   GPIO 26
rel4 = 38            # pin Relay 2 (board derecha),   GPIO 20

# setup all the pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)
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

try:
	while True:
		i=GPIO.input(pir)
		if i==0: #When output from motion sensor is LOW
			print "No intruders",i
			GPIO.output(red, 0)  #Turn OFF
			GPIO.output(rel2_giro, 1)  #Turn OFF
			GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
			time.sleep(wait)
		elif i==1: #When output from motion sensor is HIGH
			print "Intruder detected",i
			os.system('mpg321 -g 50 -q intruso_detectado.mp3')
			GPIO.output(red, 1)  #Turn ON
			GPIO.output(rel2_giro, 0)  #Turn ON
			GPIO.output(rel3_luz_sirena, 0)  #Turn ON
			os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -q --title test --no-banner /home/pi/captura_%d%m%y_%H%M%S.jpg")
			time.sleep(wait)
except KeyboardInterrupt:  
		pass

#Tidy up and remaining connections.  
GPIO.cleanup()