# -*- coding: utf-8 -*-
#Imports
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import random
import sys
import cv2
import os
import base64
#import queue
import threading
from threading import Thread
import datetime
import json
import requests


#Processamento de sinais
def proc_sinal():
	c=0
####SINALIZAÇÃO####
#Inicializanrf24_tx
def inicionrf24tx():
	pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

	radio = NRF24(GPIO, spidev.SpiDev())
	radio.begin(0, 17)
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
	r_r = 0
	r_c = 0
	rx = [r_r,r_c]
	return rx
#Transmissão de Flag
def flag_tx(deteccao):
    buf = [deteccao]
    radio.write(buf)
    if radio.isAckPayloadAvailable():
        pl_buffer=[]
        radio.read(pl_buffer, radio.getDynamicPayloadSize())
        print ("Enviado:", buf) 
        print ("Retorno:", pl_buffer)
        print("\n")
    else:
        print ("Sem conexão: 0")
    time.sleep(0.5)

#Recepção de Flag
def flag_rx(rx):
    rx[0] = r_r
    rx[1] = r_c
    akpl_buf = [r_r]
    pipe = [0]
    while not radio2.available(pipe):
       r_c = r_c + 1
       time.sleep(0.5)
       if r_c > 2:
          print("Sem conexão")
          r_c = 0
    r_c = 0
    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    print ("Recebido:", recv_buffer)
    radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
    print ("Retorna:", akpl_buf)
    print ("\n")
    r_r = r_r + 1
    return recv_buffer

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

###CÂMERA###
#Inicializa a câmera
def inicio_camera():
	## Inicialização do caminho
	path = 'Banco_de_Imagens/'
	now = datetime.now()
	data = str(now.day)+'_'+str(now.month)+'_'+str(now.year)+'/'
	dirfailed = 512# caso nao consiga criar diretorio

	## Diretório
	if os.system('cd '+ path + data) == dirfailed:
		os.system('mkdir '+ path + data)
		os.system('cd '+ path + data)

	cap = cv2.VideoCapture('rtsp://admin:radarpi2@10.0.0.100:554')    
	cap.set(1080)
	cap.set(720)
#Ativa captura
def captura():
	for i in range(2):
		ret1, frame1 = cap.read()
		ret.put(ret1)
		frame.put(frame1)
		time.sleep(0.5)

def salva_captura():
    for i in range(2):
        now = datetime.now()
        hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)+':'+str(now.microsecond)
        img1 = cv2.imwrite(path+data+hora+'.jpg', frame.get())
        print("Horário Infração: ", hora)
        print("Velocidade Infração: ", vel)
        time.sleep(0.5)
#Conversão img para base 64
def conv_img():
	img1 = base64.b64encode(file.read())
	img2 = base64.b64encode(file.read())

###SERVIDOR###
#Define o payload
def pacote():
	pacote = []
	i = 0
	for i in range(1):
         idradar = random.randrange(0,10)
         time = datetime.datetime.utcnow()
         time = str(time.isoformat('T') + 'Z')
         with open("/home/rodrigo/Documentos/Controle_Rasp/Camera/Banco_de_Imagens/19_5_2019/16:1:31:543280.jpg", "rb") as file:
             img1 = base64.b64encode(file.read())
         with open("/home/rodrigo/Documentos/Controle_Rasp/Camera/Processamento_de_Imagens/Teste2/limiar_20_sobelx.jpg", "rb") as file:
             img2 = base64.b64encode(file.read())
	lista = cont_infracao()
	vm = lista[0]
	vc = lista[1]
	infracao = lista[2]
	penalidade = lista[3]
	vr = lista[4]
	
	base = {
            "type": "dados_carro",
            "payload": {
                "id_radar":idradar,
                "infracao":infracao, 		
                "imagem1": img1,
                "imagem2": img2,
                "velocidade_medida":vm,
                "velocidade_considerada":vc,
                "velocidade_regulamentada":vr,
                "penalidade":penalidade,
                "date":time
            }
        }
	if (i==0):
	    print ("Ok")

	pacote.append(base)
	base = {}

#Salva pacote em JSON
def salva_arquivo():
    with open('data.json', 'a') as f:
        json.dump(pacote, f ,indent=2)

#Envia para servidor
def envia_arquivo():
	with open('data.json', 'r') as f: 
		r = requests.post(url, json.load(f))
		r.raise_for_status()
	return r.status_code 

r_c = 0
r_r = 0
