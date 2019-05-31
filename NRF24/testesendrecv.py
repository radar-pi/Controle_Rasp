#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
import sys



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()


radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

if not radio.isPVariant():
       radio.printDetails()
       print ("NRF24L01+ not found.")
       exit()

def envio():
    while True:
        buf = [1]
        radio.write(buf)
        print ("Enviado:", buf),
        if radio.isAckPayloadAvailable():
            pl_buffer=[]
            radio.read(pl_buffer, radio.getDynamicPayloadSize())
            print ("Retorno:", pl_buffer)
        else:
            print ("Sem conexão envio: 0")
        time.sleep(1)
 
 
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

c=1
r=1
def recebe():
    while True:
	
        akpl_buf = [r]
        pipe = [0]
        while not radio2.available(pipe):
            time.sleep(10000/1000000.0)

        recv_buffer = []
        radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
        print ("Recebido:", recv_buffer)
        c = c + 1
        if (c&1) == 0:
            radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
            print ("Retorna:", akpl_buf)
            r = r+1
        else:
            print ("Sem conexão: 0")
        time.sleep(1)
 



while True:
        envio()   # send something
        time.sleep(1)
        recebe()    # has it arrived? (if so, maybe send return data)
        time.sleep(1)   # 1 sec per loop
