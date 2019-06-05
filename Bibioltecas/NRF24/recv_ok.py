#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 17)

radio2.setRetries(15,15)

radio2.setPayloadSize(16)
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

r=0
c=0
while True:

    akpl_buf = [r]
    pipe = [0]
    while not radio2.available(pipe):
       c = c + 1
       time.sleep(0.5)
       if c > 2:
          print("Sem conexão")
          c = 0
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

