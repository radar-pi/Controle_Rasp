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
from Queue import Queue
import threading
from datetime import datetime
import json
import requests
c=0
r=0
x=0
j=0

class Processamentodesinais(object):
    def __init__(self):
		print 'Detecção e Velocidade'
    
    def proc_sinal(self,d,v):
        
        while True:
            deteccao = random.randrange(0,2)
            if deteccao == 1:
                    vm = random.randint(58,62)
		    d.put(deteccao)
		    v.put(vm)
		    time.sleep(0.2)
		    
            else:
                    vm = 0
		    d.put(deteccao)
		    v.put(vm)
		    time.sleep(1)
	    print (deteccao, vm)
	    time.sleep(0.5)   
	    #retorna detecção e velocidade;
    
class Sinalizacao(object):
    def __init__(self):
            print 'Inicio Sinalização'
            global contador
	    self.h = 0
            
	    self.rele = 14
	    GPIO.setwarnings(False)
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(self.rele, GPIO.OUT)
	    GPIO.cleanup(self.rele)
	    
	    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
	    self.radio = NRF24(GPIO, spidev.SpiDev())
	    self.radio.begin(0, 22)
	    self.radio.setRetries(15,15)
	    self.radio.setPayloadSize(32)
	    self.radio.setChannel(0x60)

	    self.radio.setDataRate(NRF24.BR_2MBPS)
	    self.radio.setPALevel(NRF24.PA_MIN)
	    self.radio.setAutoAck(True)
	    self.radio.enableDynamicPayloads()
	    self.radio.enableAckPayload()

	    self.radio.openWritingPipe(pipes[1])
	    self.radio.openReadingPipe(1, pipes[0])
	    #self.radio.printDetails()
 

	    self.radio2 = NRF24(GPIO, spidev.SpiDev())
	    self.radio2.begin(0, 22)

	    self.radio2.setRetries(15,15)

	    self.radio2.setPayloadSize(32)
	    self.radio2.setChannel(0x60)
	    self.radio2.setDataRate(NRF24.BR_2MBPS)
	    self.radio2.setPALevel(NRF24.PA_MIN)

	    self.radio2.setAutoAck(True)
	    self.radio2.enableDynamicPayloads()
	    self.radio2.enableAckPayload()

	    self.radio2.openWritingPipe(pipes[0])
	    self.radio2.openReadingPipe(1, pipes[1])

	    self.radio2.startListening()
	    self.radio2.stopListening()

	    #self.radio2.printDetails()

	    self.radio2.startListening()
        


    def flag_tx(self): #Transmissão de Flag
	    while True: 
		print 'transmite'
		flag = [1] 
		self.radio.stopListening()
		self.radio.write(flag)
		if self.radio.isAckPayloadAvailable():
		    mensagem=[]
		    self.radio.read(mensagem, self.radio.getDynamicPayloadSize())
		    print ("Enviado:", flag) 
		    print("\n")
		else:
		    #print ("Sem conexão: 0")
		    self.radio.startListening()
		self.radio.startListening()	
		return
            
    
    def flag_rx(self, s, r): #Recepção de Flag
        while True:
	    print 'recebe'
            self.radio2.startListening()
	    contador = [self.h]
            pipe = [0]
            while not self.radio2.available(pipe):
                return
            recebido = []
            self.radio2.read(recebido, self.radio2.getDynamicPayloadSize())
            print ('Recebido:', recebido)
            if recebido == [1]:
                print("Carro detectado!")
                sinalizacao = 1
            else:
		sinalizacao = 0
	    r.put(sinalizacao)
	    self.radio2.writeAckPayload(1, contador, len(contador))
            print ("Retorna:", contador)
            print ("\n")
            self.h = self.h + 1
	    return
            
	    
    def controle_rele(self,r,d):  #Controle do Relé
	
	print 'rele'
        while True:
	    sinalizacao = r.get()
	    if sinalizacao == 1:
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.rele, GPIO.OUT)
		GPIO.output(self.rele, GPIO.HIGH)
	    else:
		time.sleep(3)
		GPIO.cleanup(14)
		
            
    def tx_rx(self, d, r, s): #Envia e recebe a flag ao mesmo tempo!
        while True:
	    deteccao = d.get()
	    flagrx = threading.Thread(target = s.flag_rx, args = (s,r))
	    flagrx.setDaemon(True)
	    flagrx.start()
	    
	    if deteccao == 1:    
		flagtx = threading.Thread(target = s.flag_tx())
		flagtx.setDaemon(True)
		flagtx.start()
		time.sleep(0.2)
	    time.sleep(0.2)
	    
class Infracao(object):  #Controle de Infração
    def __init__(self):
            print 'Infracao'
            self.penalidade = 0
            self.vr = 40
            global vm

    def cont_infracao(self,v,pay):
        while True:
            vm = v.get()
	    
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

            #if(vc > self.vr):
              #  captura.start()
	    
            vinte = int (self.vr + ((20*40)/100))	
            cinquenta = int (self.vr + ((50*40)/100))

            if  vc >= self.vr and vc <= vinte:
                infracao = 1
                self.penalidade = True

            elif vc > vinte and vc <= cinquenta:
                infracao = 2
                self.penalidade = True

            elif vc > cinquenta:
                infracao = 3
                self.penalidade = True
            else:
                infracao = 0
                self.penalidade = False
            time.sleep(1)
	    lista = [vm, vc, self.vr, infracao, self.penalidade]
	    print(lista)
	    time.sleep(1)
	    pay.put(lista)
	    #servidor.start()
class Camera(object):
    def __init__(self):
        path = 'Banco_de_Imagens/'
        now = datetime.now()
        data = str(now.day)+'_'+str(now.month)+'_'+str(now.year)+'/'
        dirfailed = 512 #caso nao consiga criar diretorio
        
        if os.system('cd '+ path + data) == dirfailed:
		    os.system('mkdir '+ path + data)
		    os.system('cd '+ path + data)

    def streaming(self, c):
        while True:
            cap = cv2.VideoCapture('rtsp://admin:radarpi2@10.0.0.100:554')    
            c.put(cap)
	    print 'stream'
    
    def captura(self,c):
        cap = c.get()
        ret, frame = cap.read()
        now = datetime.now()
        hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)+':'+str(now.microsecond)
        imagem = cv2.imwrite(path+data+hora+'.jpg', frame)
        print("Horário Infração: ", hora)
        print("Velocidade Infração: ", vel)
        img.put(imagem)
	return
 
class Servidor(object):
    def __init__(self):
	print 'Servidor'
        global vr
        global penalidade
        self.id_radar = 2019
        self.time = datetime.datetime.utcnow()
        self.time = str(time.isoformat('T') + 'Z')
    def dados(self,lista):
        vm = lista[0]
        vc = lista[1]
        vr = lista[2]
        infracao = lista[3]
        penalidade = lista[4]
        img = lista [5]
	pacote = []
        base = {
            "type": "dados_carro",
            "payload": {
                "id_radar":self.idradar,
                "infracao":infracao, 		
                "imagem1": img1,
                #"imagem2": img2,
                "velocidade_medida":vm,
                "velocidade_considerada":vc,
                "velocidade_regulamentada":vr,
                "penalidade":penalidade,
                "date":self.time
		}
	    }
        with open('data.json', 'a') as f:
            json.dump(pacote, f ,indent=2)
        with open('data.json', 'r') as f: 
	    r = requests.post(url, json.load(f))
	    r.raise_for_status()
	return r.status_code 

def main():
 
    #Variáveis que compartilham Threads
    v = Queue(maxsize=0) #velocidade
    d = Queue(maxsize=0) #deteccao
    r = Queue(maxsize=0) #sinalização
    c = Queue(maxsize=0) #captura
    pay = Queue(maxsize=0) #payload

    #Simplicação das Classes
    p = Processamentodesinais()
    s = Sinalizacao()
    i = Infracao()
    f = Camera()
    q = Servidor
    
    procsinal = threading.Thread(target=p.proc_sinal, args=(d,v))
    procsinal.setDaemon(True)
    procsinal.start()
	
    flag = threading.Thread(target= s.tx_rx, args = (d,r,s))
    flag.setDaemon(True)
    flag.start()
    
    time.sleep(1)
    
    rele = threading.Thread(target = s.controle_rele, args =(r,d))
    rele.setDaemon(True)
    rele.start()
    
    infracao = threading.Thread(target = i.cont_infracao, args = (v,pay))
    infracao.setDaemon(True)
    infracao.start()
    
    #stream = threading.Thread(target = f.streaming, args = (c))
    #stream.setDaemon(True)
    #stream.start()
    
    #capture = threading.Thread(target = f.captura, args = (c))
    #capture.setDaemon(True)
    #capture.start()
    
	

    print 'Procsinall'
    time.sleep(0.5)
    
    while True:
	pass

	  
    
if __name__ == '__main__':
	
       
    #Abertura da função principal
    main()

