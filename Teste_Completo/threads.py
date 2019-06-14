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
import datetime
import json
import requests
c=0
r=0
x=0
j=0

class Processamentodesinais(object):
    def __init__(self):
		print 'Detecção e Velocidade'
    
    def proc_sinal(self,d,f,c,p,s):
        
        while True:
            deteccao = random.randrange(0,2)
            if deteccao == 1:
                    vm = random.randint(58,62)
            else:
                    vm = 0
                   
            d.put(deteccao)
            lista = i.cont_infracao(vm,f,c,s)
            time.sleep(1)   

    #retorna detecção e velocidade;
    
class Sinalizacao(object):
    def __init__(self):
            print 'Inicio Sinalização'
            self.contador = 0
            self.rele = 14
    
    def inicionrf24tx(self): # Inicializa transmissão do módulo NRF24;
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
        return radio

    def inicionrf24rx(self): # Inicializa recepção do módulo NRF24;
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


    def flag_tx(self,radio,deteccao): #Transmissão de Flag
	    while True: 
		    flag = [deteccao] 
		    radio.stopListening()
            radio.write(flag)
            if radio.isAckPayloadAvailable():
                mensagem=[]
                radio.read(mensagem, radio.getDynamicPayloadSize())
                print ("Enviado:", flag) 
                print("\n")
            else:
                #print ("Sem conexão: 0")
                radio.startListening()
            radio.startListening()	
            time.sleep(0.24)
            
    
    def flag_rx(self,radio2,r): #Recepção de Flag
        while True:
            radio2.startListening()
            pipe = [0]
            while not radio2.available(pipe):
                return
            recebido = []
            radio2.read(recebido, radio2.getDynamicPayloadSize())
            print ('Recebido:', recebido)
            if recebido == [1]:
                print("Carro detectado!")
                sinalizacao = 1
                               
            else:
                sinalizacao = 0
                
            r.put(sinalizacao)       
            radio2.writeAckPayload(1, contador, len(contador))
            print ("Retorna:", contador)
            print ("\n")
            self.contador = self.contador + 1
            print(self.contador)
            time.sleep(0.24)
            		
    def controle_rele(self,r):  #Controle do Relé
        sinalizacao = r.get()
        while sinalizacao == 1:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.rele, GPIO.OUT)
            GPIO.output(self.rele, GPIO.HIGH)
            sinalizacao = r.get()
        time.sleep(2)
        GPIO.cleanup(14)
            
    def tx_rx(self, d, radio, radio2, r): #Envia e recebe a flag ao mesmo tempo!
        while True:
            deteccao = d.get()
            flag_tx(radio,deteccao)
            time.sleep(0.1)
            flag_rx(radio2, r)
            time.sleep(0.1)
    
    def leitura(self,v,d,r):
        while True:
            print (d.get())
            print (r.get())
            print ('\n')
            time.sleep(0.25)

class Infracao(object):  #Controle de Infração
    def __init__(self):
            print 'Infracao'
            self.penalidade = 0
            self.vr = 40
            global vm

    def cont_infracao(self,vm,f,c,s):
        while True:
            
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
                img = f.captura(c)


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
            lista = [vm, vc, self.vr, infracao, self.penalidade, img]

            #THREAD Servidor
            maestro = threading.Thread(target= s.dados(self,lista))
            maestro.setDaemon(True)
            #maestro.start()

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
    
    def captura(self,c):
        cap = c.get()
        ret, frame = cap.read()
        now = datetime.now()
        hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)+':'+str(now.microsecond)
        img = cv2.imwrite(path+data+hora+'.jpg', frame)
        print("Horário Infração: ", hora)
        print("Velocidade Infração: ", vel)
        return img
 
class Servidor(object):
    def __init__(self):
        global vr
        global penalidade
        self.id_radar = 2019
        self.time = datetime.datetime.utcnow()
        self.time = str(time.isoformat('T') + 'Z')
    def dados(self,lista)
        vm = lista[0]
        vc = lista[1]
        vr = lista[2]
        infracao = lista[3]
        penalidade = lista[4]
        img = lista [5]

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

        with open('data.json', 'a') as f:
            json.dump(pacote, f ,indent=2)
        with open('data.json', 'r') as f: 
		    r = requests.post(url, json.load(f))
		    r.raise_for_status()
	    return r.status_code 

def main():
 
    #Variáveis que compartilham Threads
    d = Queue(maxsize=0) #deteccao
    r = Queue(maxsize=0) #sinalização
    c = Queue(maxsize=0) #captura
    p = Queue(maxsize=0) #payload

    #Simplicação das Classes
    p = Processamentodesinais()
    s = Sinalizacao()
    i = Infracao()
    f = Camera()
    s = Servidor

    #Inicio das funções que rodarão apenas uma vez
    radio = s.inicionrf24tx()
    radio2 = s.inicionrf24rx()

    #THREAD PROCESSAMENTO DO SINAL
    procsinal = threading.Thread(target=p.proc_sinal, args=(d,v,f,c,p,s))
    procsinal.setDaemon(True)
   
    #THREAD TX E RX NRF24
    flag = threading.Thread(target= s.tx_rx(d, radio, radio2,r))
    flag.setDaemon(True)
     
    #THREAD RELÉ
    rele = threading.Thread(target= s.controle_rele(r))
    rele.setDaemon(True)

    #Streaming da câmera
    stream = threading.Thread(target=f.streaming(c))
    stream.setDaemon(True)

    #Teste de retorno de flag
    p2 = threading.Thread(target = s.leitura, args=(v,d,r))
    p2.setDaemon(True)
    
    #Start Threads
    procsinal.start() #Processamento de sinais
    time.sleep(0.1)
    flag.start()    #Tx_RX
    time.sleep(0.1)
    rele.start()   #Sinalização
    time.sleep(0.1)
    stream.start()  #Câmera streaming
    time.sleep(0.1)
    p2.start()  #Leitura de dados

    while True:
        pass

if __name__ == '__main__':
	
    #Abertura da função principal
    main()


