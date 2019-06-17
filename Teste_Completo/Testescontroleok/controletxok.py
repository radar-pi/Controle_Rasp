# -*- coding: utf-8 -*- Imports
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
import sys
#import cv2
#import os
#import base64
#import queue
import threading
import datetime
#import json
#import requests




#Processamento de sinais
def proc_sinal():
	c=0
####SINALIZAÇÃO####
#Inicializanrf24_tx
def inicionrf24tx():
	pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

	radio = NRF24(GPIO, spidev.SpiDev())
	radio.begin(0, 17)
	time.sleep(1)
	radio.setRetries(15,15)
	radio.setPayloadSize(16)
	radio.setChannel(0x60)

	radio.setDataRate(NRF24.BR_2MBPS)
	radio.setPALevel(NRF24.PA_MIN)
	radio.setAutoAck(True)
	radio.enableDynamicPayloads()
	radio.enableAckPayload()


	radio.openWritingPipe(pipes[1])
	radio.openReadingPipe(1, pipes[0])
	radio.printDetails()
	return radio

def inicionrf24rx():
	pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

	radio2 = NRF24(GPIO, spidev.SpiDev())
	radio2.begin(0, 17)

	radio2.setRetries(15,15)

	radio2.setPayloadSize(32)
	radio2.setChannel(0x60)
	radio2.setDataRate(NRF24.BR_2MBPS)
	radio2.setPALevel(NRF24.PA_MIN)

	radio2.setAutoAck(True)
	radio2.enableDynamicPayloads()
	radio2.enableAckPayload()

	radio2.openWritingPipe(pipes[0])
	radio2.openReadingPipe(1, pipes[1])

	radio2.startListening()
	radio2.stopListening()

	radio2.printDetails()

	radio2.startListening()
	return radio2

#Transmissão de Flag
def flag_tx(radio):
	while True:
   
		x = random.randrange(0,2)
		buf = [x] 
		inicio = time.time()
		radio.write(buf)
		if radio.isAckPayloadAvailable():
			pl_buffer=[]
			radio.read(pl_buffer, radio.getDynamicPayloadSize())
			fim = time.time()
			print ("Enviado:", buf) 
			print ("Retorno:", pl_buffer)
			print ("Tempo:", fim-inicio)
			print("\n")
		else:
			print ("Sem conexão: 0")
		time.sleep(0.5)

#Recepção de Flag
def flag_rx(radio2, c_rx,r_rx):
	while True:
		print("Recebendo")
		#print("Começa flagrx")
		c = c_rx
		r = r_rx
		akpl_buf = [r]
		pipe = [0]
		while not radio2.available(pipe):
			c = c + 1
			if c > 2:
			  #print("Sem conexão!")
			  c = 0
			  time.sleep(1)
		c = 0
		recv_buffer = []
		radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
		print ("Recebido:", recv_buffer)
		if recv_buffer == [1]:
			sinalizacao = 1
		else:
			sinalizacao = 0
		print("Sinalizacao:", sinalizacao)
		radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
		print ("Retorna:", akpl_buf)
		print ("\n")
		r = r + 1
		time.sleep(0.2)

#Controle do Relé
def controle_rele():
	c=0
###CONTROLE DE INFRAÇÃO###
def cont_infracao():
	infracao1 = 0
#	vm = int(random.randrange(20,150))
#	vr = int(random.randrange(40,80,20))

	if vm >= 27 and vm <= 107:
		vc = vm - 7
	elif vm >= 108 and vm <= 121:
		vc = vm - 8
	elif vm >= 122 and vm <= 135:
		vc = vm - 9
	elif vm >= 136 and vm <= 150:
		vc = vm - 10
	elif vm >= 151 and vm <= 161:
		vc = vm - 11
	else:
		vc = vm

	vinte = int (vr + ((20*40)/100))	
	cinquenta = vr + ((50*40)/100)

	if  vc >= vr and vc <= vinte:
		infracao1 = 1
		penalidade = True

	elif vc > vinte and vc <= cinquenta:
		infracao1 = 2
		penalidade = True

	elif vc > cinquenta:
		infracao1 = 3
		penalidade = True
	else:
		infracao = 0

radio = inicionrf24tx()
#radio2 = inicionrf24rx()


#c_tx=0
#while True:
	
	#deteccao = random.randint(0,1)
	#deteccao  = input("Detec:")
	
	#print("Detecção:", deteccao)
	#t_rx = threading.Thread(target=flag_rx, args=(radio2, c_rx, r_rx), daemon = True)
t_tx = threading.Thread(target=flag_tx(radio))


	#if deteccao == 1:
t_tx.start()
	#	t_rx.start()
	#	i = i+1
	#else:
	#	t_rx.start()
		
time.sleep(2)


