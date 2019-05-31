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


radio_tx = NRF24(GPIO, spidev.SpiDev())
radio_tx.begin(0, 17)
radio_tx.setRetries(15,15)
radio_tx.setPayloadSize(32)
radio_tx.setChannel(0x60)

radio_tx.setDataRate(NRF24.BR_2MBPS)
radio_tx.setPALevel(NRF24.PA_MIN)
radio_tx.setAutoAck(True)
radio_tx.enableDynamicPayloads()
radio_tx.enableAckPayload()

radio_tx.openWritingPipe(pipes[1])
radio_tx.openReadingPipe(1, pipes[0])
radio_tx.printDetails()

radio_rx = NRF24(GPIO, spidev.SpiDev())
radio_rx.begin(0, 17)

radio_rx.setRetries(15,15)

radio_rx.setPayloadSize(32)
radio_rx.setChannel(0x60)
radio_rx.setDataRate(NRF24.BR_2MBPS)
radio_rx.setPALevel(NRF24.PA_MIN)

radio_rx.setAutoAck(True)
radio_rx.enableDynamicPayloads()
radio_rx.enableAckPayload()

radio_rx.openWritingPipe(pipes[0])
radio_rx.openReadingPipe(1, pipes[1])

radio_rx.startListening()
radio_rx.stopListening()

radio_rx.printDetails()

radio_rx.startListening()

def envio():


    buf = [1]
    radio_tx.write(buf)
    print ("Enviado:", buf),
    if radio_tx.isAckPayloadAvailable():
        pl_buffer=[]
        radio_tx.read(pl_buffer, radio_tx.getDynamicPayloadSize())
        print ("Retorno:", pl_buffer)
    else:
        print ("Sem conexão envio: 0")

def recebe():
    c=1
    r=1
   
	
    akpl_buf = [r]
    pipe = [0]
    while not radio_rx.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio_rx.read(recv_buffer, radio_rx.getDynamicPayloadSize())
    print ("Recebido:", recv_buffer)
    c = c + 1
    if (c&1) == 0:
        radio_rx.writeAckPayload(1, akpl_buf, len(akpl_buf))
        print ("Retorna:", akpl_buf)
        r = r+1
    else:
        print ("Sem conexão: 0")

while True:
    envio()   # send something
    time.sleep(1)
    recebe()    # has it arrived? (if so, maybe send return data)
    time.sleep(1)   # 1 sec per loop
