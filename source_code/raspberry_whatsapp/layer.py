#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, time
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)  # Turn off warnings
GPIO.setmode(GPIO.BOARD) # Config as BOARD

# Pins
red = 12             # pin RGB LED, GPIO 18
green = 16           # pin RGB LED, GPIO 23
blue = 18            # pin RGB LED, GPIO 24
pir = 32             # pin PIR sensor, GPIO 12
rel1_sirena = 35     # pin Relay 1 (board izquierda), GPIO 19
rel2_giro = 36       # pin Relay 2 (board izquierda), GPIO 16
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

# INIT
GPIO.output(red, 0)  #Turn OFF LED
GPIO.output(green, 0)  #Turn OFF LED
GPIO.output(blue, 0)  #Turn OFF LED
GPIO.output(rel1_sirena, 1)  #Turn OFF
GPIO.output(rel2_giro, 1)  #Turn OFF
GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
GPIO.output(rel4, 1)  #Turn OFF

from yowsup.layers                                     import YowLayer
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
 
class EchoLayer(YowInterfaceLayer):

	@ProtocolEntityCallback("message")
	def onMessage(self, messageProtocolEntity):

		if messageProtocolEntity.getType() == 'text':
			self.onTextMessage(messageProtocolEntity)

		self.toLower(messageProtocolEntity.ack())
		self.toLower(messageProtocolEntity.ack(True))


	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		print "ack: ", entity.ack()
		self.toLower(entity.ack())


	def onTextMessage(self,messageProtocolEntity):

		nombre  = messageProtocolEntity.getNotify()
		mensaje = messageProtocolEntity.getBody()
		para    = messageProtocolEntity.getFrom()
		# escribir en siguiente linea el telefono desde donde se envian ordenes
		if para == '346xxxxxxxx@s.whatsapp.net':
			if mensaje=='Hola Pi':
				msg_txt = "Hola Fran como va la NcN2k15 ?" 
				print msg_txt
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
			elif mensaje == 'Bien gracias':
				msg_txt = "Me alegra. ¿Qué deseas hacer?"
				msg_txt2 = "0. Para apagar sirena.\n1. Para encender sirena."
				print msg_txt
				print msg_txt2
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
				self.toLower(TextMessageProtocolEntity( msg_txt2, to = para ))
			elif mensaje == '1':
				msg_txt = "Opción 1. La sirena se ha encendido"
				print msg_txt
				GPIO.output(rel3_luz_sirena, 0)  #Turn ON
				GPIO.output(rel2_giro, 0)  #Turn ON
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
			elif mensaje == '0':
				msg_txt = "Opción 0. La sirena se ha apagado"
				print msg_txt
				GPIO.output(rel3_luz_sirena, 1)  #Turn OFF
				GPIO.output(rel2_giro, 1)  #Turn OFF
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
			elif mensaje == '\xF0\x9F\x9A\xA8':
				msg_txt = "Sirena!"
				print msg_txt
				GPIO.output(rel3_luz_sirena, 0)  #Turn ON
				GPIO.output(rel2_giro, 0)  #Turn ON
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
			elif mensaje == '\xF0\x9F\x94\xAB':
				os.system('mpg321 -g 100 -q mob_ua-gun_shoot_m_16.mp3 &')
			else:
				msg_txt = "No entiendo !"
				print msg_txt
				self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))
		else:
			msg_txt = "¿Qué estás intentando " + nombre + " ? ¿Te parece bonito?"
			print msg_txt
			self.toLower(TextMessageProtocolEntity( msg_txt, to = para ))