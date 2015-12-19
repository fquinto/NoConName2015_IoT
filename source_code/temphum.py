#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author     Version      Date        Comments
# FQuinto    1.0.0        2015-Nov    First version fron NoConName 2015 event

# Get temperature and humidity data
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

import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# Pins
temphum = 2 # GPIO2, pin 3

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, temphum)

# success:true,temperature:18.6,humidity:55.8

if humidity is not None and temperature is not None:
	print 'temperature:{0:0.1f},humidity:{1:0.1f}'.format(temperature, humidity)
else:
	print 'temperature:0,humidity:0'