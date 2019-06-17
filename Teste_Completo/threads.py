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


class Processamentodesinais(object):
    def __init__(self):
		print 'Detecção e Velocidade'
    
    def proc_sinal(self,d,v):
        
        while True:
            #deteccao = random.randrange(0,2)
            deteccao = 1
	    if deteccao == 1:
                    vm = random.randint(58,62)
		    #vm = input('Velocidade:' )
		    d.put(deteccao)
		    v.put(vm)
		    #print('Velocidade: ')
		    #print(datetime.utcnow())
		    #print('Deteccao: ', deteccao)
            #else:
                    #vm = 0
		    #d.put(deteccao)
		    #v.put(vm)
	    time.sleep(2)
class Sinalizacao(object):
    def __init__(self):
            print 'Inicio Sinalização'
            global contador
	    self.h = 0
            self.contador = 0
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
	    self.radio.printDetails()
 

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

	    self.radio2.printDetails()

	    self.radio2.startListening()

        


    def flag_tx(self): #Transmissão de Flag
	    while True: 
		#print 'transmite'
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
            
    
    def flag_rx(self, s, r,d, cont): #Recepção de Flag
        while True:
	    #print ('recebe')
	   
            contador = [self.h]
            pipe = [0]
	    if self.radio2.available(pipe):
    
		recebido = []
		self.radio2.read(recebido, self.radio2.getDynamicPayloadSize())
		print ('Recebido:', recebido)
		if recebido == [1]:
		    print("Carro detectado!")
		    sinalizacao = 1
		    r.put(sinalizacao)
		    self.contador = self.contador + 1
		    print('antes', self.contador)
		    cont.put(self.contador)
		    rele = threading.Thread(target = s.controle_rele, args =(r,d, cont))
		    rele.setDaemon(True)
		    rele.start()
		    print('depois', self.contador)

		#else:
		#   sinalizacao = 0
		self.radio2.writeAckPayload(1, contador, len(contador))
		print ("\n")
		self.h = self.h + 1
	    return
		
	    
    def controle_rele(self,r,d, cont):  #Controle do Relé
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(self.rele, GPIO.OUT)
	GPIO.output(self.rele, GPIO.HIGH)
    	time.sleep(5)
	print 'passou 5 segundos'
	cont_depois = cont.get()
	
	if self.contador == cont_depois:
	    GPIO.cleanup(self.rele)
	return


	
		
            
    def tx_rx(self, d, r, s, cont, opnrf): #Envia e recebe a flag ao mesmo tempo!
        while True:
	    if self.radio2.getCRCLength() == NRF24.CRC_DISABLED:
		opnrf.put(False)
	    else:
		opnrf.put(True)
	    deteccao = d.get()
	    #print ('tx_rx',deteccao)
	    flagrx = threading.Thread(target = s.flag_rx, args = (s,r,d, cont))
	    flagrx.setDaemon(True)
	    flagrx.start()
	    
	    if deteccao == 1:    
		flagtx = threading.Thread(target = s.flag_tx())
		flagtx.setDaemon(True)
		flagtx.start()
		time.sleep(0.2)
	    
class Infracao(object):  #Controle de Infração
    def __init__(self):
            print 'Infracao'
            self.penalidade = 0
            self.vr = 40
            global vm

    def cont_infracao(self,v, pay, f, c, q, d, img1): #Inserir captura
        while True:
	    #print 'Abre Infracao'
	    #print 'x'
	    d#eteccao = d.get()
	    #print (deteccao)
	    #if deteccao == 1:
	    vm = v.get()
	    #print (vm)
	    
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
	    
	    if(vc > self.vr):
		#print('Carro infrator')
		f.captura(c, vc, img1)
	   
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
		
		lista = [vm, vc, self.vr, infracao, self.penalidade]
	    #print(lista)
	    #pay.put(lista)
	    #print 'Chama servidor\n'
		q.veiculo(pay, lista, img1)
	    else:
		a = 0
		#print('Velocidade considerada: ', vc)
		#print('Carro abaixo do limite da via')
		
class Camera(object):
    def __init__(self):
        self.path = 'Banco_de_Imagens/'
        self.now = datetime.now()
        self.data = str(self.now.day)+'_'+str(self.now.month)+'_'+str(self.now.year)+'/'
        dirfailed = 512 #caso nao consiga criar diretorio
        
        if os.system('cd '+ self.path + self.data) == dirfailed:
		    os.system('mkdir '+ self.path + self.data)
		    os.system('cd '+ self.path + self.data)

    def streaming(self, c, opcam):
        while True:
	    #print 'Roda câmera\n'
	    cap = cv2.VideoCapture('rtsp://admin:radarpi2@10.0.0.100:554')
	    opcam.put(cap.isOpened())
	    # Returns true if video capturing has been initialized already.
            c.put(cap)

    
    def captura(self, c, vc, img1): 
	    #print 'Faz a captura\n'
	    cap = c.get()
	    ret, frame = cap.read()
	    self.now = datetime.now()
	    self.hora = str(self.now.hour)+':'+str(self.now.minute)+':'+str(self.now.second)+':'+str(self.now.microsecond)
	    imagem = cv2.imwrite(self.path+self.data+self.hora+'.jpg', frame)
	    #print('Salva imagem',datetime.utcnow())
	    #print("Horario: ", self.hora)
	    #print("Velocidade", vc)
	    img1.put(frame)
	    return frame

#class Processamentodeimagem(object)
    # def __init__(self):
    #Passar parâmetro carro
    #carro.start()

class Servidor(object):
    def __init__(self):
	print 'Servidor\n'
        global vr
        global penalidade
        self.id_radar = 2019
	self.x = 0

    def veiculo(self, pay, lista, img1): #colocar img 2
        #print 'Abre o Servidor\n'
	#lista = pay.get()
        vm = lista[0]
        vc = lista[1]
        vr = lista[2]
        infracao = lista[3]
        penalidade = lista[4]
        imagem = base64.b64encode(img1.get())
        
	veiculo = {
        "id_radar": self.id_radar,
        "infraction": infracao,
        #"image1": img1,
        #"image2": img1,
        "vehicle_speed": vm,
        "considered_speed": vc,
        "max_allowed_speed": vr 
    }
	#print('FIM', datetime.utcnow())
	#print (veiculo)
	return
	
	
	#vehicle_flagrant_msg.send_vehicle_flagrant(veiculo)
    
    def operacionalidade(self, opcam, opras,opusr, opnrf):
        
        while True:
	    print 'Operacionalidade'
	    camera = opcam.get()
	    nrf = opnrf.get()
	    print (camera)
	    print (nrf)
	    print self.x
	    print camera and nrf
	    print self.x == 0
	    if (camera and nrf == True) and (self.x == 0) == True:
		print 'Envia'
		x = 1
	    if (camera and nrf == False):
		print 'Envia erro'
		x = 0
	    
        #rasp = opras.get()
        #usrp = opusrp.get()
        
       # if (usrp and rasp and camera) == 1:
        #    func_geral = True
        #else:
        #    func_geral = False
        
        
	    operacionalidade = {
	    "radar_id": self.id_radar,
	    "camera": camera,
	    "nrf24": nrf
	    #"rasp": raspberry,
	    #"usrp": usrp,
	    #"radar": func_geral
	}

    #status_radar_msg.send_status_radar(operacionalidade)

def main():
 
    #Variáveis que compartilham Threads
    v = Queue(maxsize=0) #velocidade
    d = Queue(maxsize=0) #deteccao
    r = Queue(maxsize=0) #sinalização
    c = Queue(maxsize=0) #captura
    pay = Queue(maxsize=0) #payload
    img1 = Queue(maxsize=0) #Imagem original
    #img2 = Queue(maxsize=0) #Imagem processada
    opcam = Queue(maxsize=0) #Operacionalidade câmera
    opras = Queue(maxsize=0) #Operacionalidade Raspberry Pi
    opusr = Queue(maxsize=0) #Operacionalidade USRP 
    opnrf = Queue(maxsize=0) #Operacionalidade NRF
    cont  = Queue(maxsize=0) #Contador pra iluminação
    #Simplicação das Classes
    p = Processamentodesinais()
    s = Sinalizacao()
    i = Infracao()
    f = Camera()
    q = Servidor()
    
    procsinal = threading.Thread(target=p.proc_sinal, args=(d,v))
    procsinal.setDaemon(True)
    procsinal.start()
    
    flag = threading.Thread(target= s.tx_rx, args = (d,r,s, cont, opnrf))
    flag.setDaemon(True)
    flag.start()
    
    time.sleep(0.2)
    

   
    infracao = threading.Thread(target = i.cont_infracao, args = (v, pay, f, c, q, d, img1)) #Adicionar captura
    infracao.setDaemon(True)
    infracao.start()
    
    stream = threading.Thread(target = f.streaming, args = (c,opcam))
    stream.setDaemon(True)
    stream.start()
     
    #carro = threading.Thread(target = q.veiculo, args = (pay, img1, img2))
    #carro.setDaemon(True) 
    
    opera = threading.Thread(target = q.operacionalidade, args = (opcam, opras, opusr, opnrf))
    opera.setDaemon(True)
    opera.start()
      
    while True:
	    pass


if __name__ == '__main__':
	       
    #Abertura da função principal
    main()
