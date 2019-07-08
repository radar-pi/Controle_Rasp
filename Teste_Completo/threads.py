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
import vehicle_flagrant_msg
import status_radar_msg


class Processamentodesinais(object):
    
    def __init__(self):
	self.vm = 0
	print ("Proc_Sinais")
	
    def proc_sinal(self,d,v):
        
        while True:
            #vm = random.randint(58,62)
	    
	    vm = input()
	    deteccao = 1
	    
	    d.put(deteccao)
	    v.put(vm)
	    print('Velocidade: ', vm)
	    
	                  
class Sinalizacao(object):
    
    def __init__(self):
        
	global contador
        self.h = 0
        self.contador = 0
	self.rele = 15
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
	self.radio.setPALevel(NRF24.PA_MAX)
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
	self.radio2.setPALevel(NRF24.PA_MAX)

	self.radio2.setAutoAck(True)
	self.radio2.enableDynamicPayloads()
	self.radio2.enableAckPayload()

	self.radio2.openWritingPipe(pipes[0])
	self.radio2.openReadingPipe(1, pipes[1])

	self.radio2.startListening()
	self.radio2.stopListening()

	self.radio2.printDetails()

	self.radio2.startListening()

        

    def flag_tx(self): #Transmite flag
	    
	    #time.sleep(0.05)
	    #print "Trasmitindo"
	    #time.sleep(0.05)
	    flag = [1]
            self.radio.stopListening()
            self.radio.write(flag)
            if self.radio.isAckPayloadAvailable():
                mensagem=[]
                self.radio.read(mensagem, self.radio.getDynamicPayloadSize())
	    else:
                #print ("Sem conexão: 0")
                self.radio.startListening()
	    self.radio.startListening()	
            return 
    
    def flag_rx(self, s, r,d, cont): #Recepção de Flag
        
	while True:
	    
	    #time.sleep(0.05)
	    #print ('Recebendo')
	    #time.sleep(0.05)
	    
            contador = [self.h]
            pipe = [0]
	    if self.radio2.available(pipe):
		recebido = []
		self.radio2.read(recebido, self.radio2.getDynamicPayloadSize())
		if recebido == [1]:
		    time.sleep(0.05)
	    	    print("Carro detectado!")
		    time.sleep(0.05)
	    	    sinalizacao = 1
		    r.put(sinalizacao)
		    self.contador = self.contador + 1
		    cont.put(self.contador)
		    rele = threading.Thread(target = s.controle_rele, args =(r,d, cont))
		    rele.setDaemon(True)
		    rele.start()
		self.radio2.writeAckPayload(1, contador, len(contador))
		self.h = self.h + 1
		time.sleep(0.1)
	    deteccao = d.get()
	    
	    if deteccao == 1:
		s.flag_tx()
		deteccao = 0
		d.put(deteccao)
	    return
	    
	
    def controle_rele(self,r,d, cont):  #Controle do Relé
	
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rele, GPIO.OUT)
        GPIO.output(self.rele, GPIO.LOW)
        time.sleep(5)
        cont_depois = cont.get()
        
        if self.contador == cont_depois:
            GPIO.output(self.rele, GPIO.HIGH)
        return


    def tx_rx(self, d, r, s, cont, opnrf): #Envia e recebe a flag ao mesmo tempo!
        
	while True:

	    if self.radio2.getCRCLength() == NRF24.CRC_DISABLED:
		opnrf.put(False)
	    else:
		opnrf.put(True)
	    
	    flagrx = threading.Thread(target = s.flag_rx, args = (s,r,d, cont))
	    flagrx.setDaemon(True)
	    flagrx.start()
	    time.sleep(0.25)

	    
class Infracao(object):  #Controle de Infração
    
    def __init__(self):
            self.vr = 40
            global vm
	    
    def cont_infracao(self,v, f, opcam, w, q):
	
        while True:
            #print 'Abre Infracao'
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
            
            if(vc > self.vr):
		time.sleep(0.05)
		print('Carro infrator')
                time.sleep(0.05)
		
		#img1 = f.captura(opcam, vm)
		
		img1 = cv2.imread("/home/pi/Documents/Controle_Rasp/Teste_Completo/teste.jpg")
		vinte = int (self.vr + ((20*40)/100))	
                cinquenta = int (self.vr + ((50*40)/100))

                if  vc >= self.vr and vc <= vinte:
                    infracao = 1
                   
                elif vc > vinte and vc <= cinquenta:
                    infracao = 2
                    
                elif vc > cinquenta:
                    infracao = 3
                    
                lista = [vm, vc, self.vr, infracao]
                
		w.processaimg(lista, q, img1)
            
	    else:
                time.sleep(0.05)
	    	print('Carro abaixo do limite da via')
		time.sleep(0.05)
	    
class Camera(object):
    
    def __init__(self):
        self.distancia = 12
	self.path = 'Banco_de_Imagens/'
        self.now = datetime.now()
        self.data = str(self.now.day)+'_'+str(self.now.month)+'_'+str(self.now.year)+'/'
        dirfailed = 512 #caso nao consiga criar diretorio
        
        if os.system('cd '+ self.path + self.data) == dirfailed:
		    os.system('mkdir '+ self.path + self.data)
		    os.system('cd '+ self.path + self.data)
	
    def captura(self, opcam,vm):
	    tempo = self.distancia/(vm/3.6)
	    #time.sleep(tempo)
	    cap = cv2.VideoCapture('rtsp://admin:radarpi2@172.20.10.6:554')
	    opcam.put(cap.isOpened())
	    print ('Faz a captura')
	    
	    ret, frame = cap.read()
	    self.now = datetime.now()
	    self.hora = str(self.now.hour)+':'+str(self.now.minute)+':'+str(self.now.second)+':'+str(self.now.microsecond)
	    imagem = cv2.imwrite(self.path+self.data+self.hora+'.jpg', frame)
	    print('Salva imagem')
	    return frame

class Processamentodeimagem(object):
    def __init__(self):
         
        self.GH = 100 # horizontal gradient 
        self.GV = 100 # vertical gradient

        #kernel for morphological tophat
        self.kernel_th = cv2.getStructuringElement(cv2.MORPH_RECT,(23,23))#need adjustment
        #kernel for morphological opening
        self.kernel_o = cv2.getStructuringElement(cv2.MORPH_RECT,(23,8))#need adjustment
        #kernel for morphological closing
        self.kernel_c = cv2.getStructuringElement(cv2.MORPH_RECT,(23,8S))#need adjustment

    def processaimg(self, lista,q, img1):

        #first load and grayscale
        img_origin = img1
        img_op = img_origin
        
	img_op = cv2.cvtColor(img_op, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("/home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_op.jpg",img_op)
        #img_op = cv2.blur(img_op,(3,3))

        # morphological top-hat
        img_op1 = cv2.morphologyEx(img_op, cv2.MORPH_TOPHAT, self.kernel_th)
        #cv2.imwrite('img_op.jpg',img_op)

        #Binarization with OTSU method
        ret2,thr = cv2.threshold(img_op1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #cv2.imwrite('thr.jpg',thr) 

        #Opening --> closing
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, self.kernel_o)
        op_cl = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.kernel_c)
        #cv2.imwrite('op_cl.jpg',op_cl)

        IMG = cv2.Canny(op_cl,self.GH,self.GV)
        _ , contours, _ = cv2.findContours(op_cl, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1 )
        cv2.drawContours(img_origin, contours, -1, (0,255,0), 3)
        cv2.imwrite('/home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_origin.jpg',img_origin)
       	
	
	vm = lista[0]
        vc = lista[1]
        vr = lista[2]
        infracao = lista[3]
	
	servidor = threading.Thread(target = q.veiculo,  args=(vm,vc,vr,infracao))
	servidor.setDaemon(True)
	servidor.start()
	return
	
class Servidor(object):
    def __init__(self):
	print ('Servidor\n')
        global vr
        global penalidade
        self.id_radar = 2019
	self.x = 0

    def veiculo(self, vm,vc,vr,infracao): 
        print 'Abre o Servidor\n'

	os.system("jpegoptim --size=300k /home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_op.jpg")
	os.system("jpegoptim --size=300k /home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_origin.jpg")
        
	with open("/home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_op.jpg", "rb") as img_file:
	    img1 = base64.b64encode(img_file.read())
	
	with open("/home/pi/Documents/Controle_Rasp/Teste_Completo/Imagens/img_origin.jpg", "rb") as img_file:
	    img2 = base64.b64encode(img_file.read())
	

	#'''	
    	#veiculo = {
        #"id_radar": self.id_radar,
        #"infraction": infracao,
        #"image1": img1,
        #"image2": img2,
        #"vehicle_speed": vm,
        #"considered_speed": vc,
        #"max_allowed_speed": vr 
        # }
	 
        veiculo = {
	    "id_radar": self.id_radar,
	    "infraction": infracao,
	    "image1": img1,
	    "image2": img2,
	    "vehicle_speed": vm,
	    "considered_speed": vc,
	    "max_allowed_speed": vr 
	    }
	
	print ('inicioflagrante')
	vehicle_flagrant_msg.send_vehicle_flagrant(veiculo)
        print ('fimflagrante')
	
    def operacionalidade(self, opcam, opusrp, opnrf):
        
	while True:
	    
	    #camera = opcam.get()
	    camera = False
	    nrf= opnrf.get()
	    opusrp = False
	    func_geral = False
	    x = True
	    
	    if (nrf and camera and x) == True: 
	    
		dado_operacionalidade = {
		    "radar_id": self.id_radar,
		    "status_camera": camera,
		    "status_rasp": nrf,
		    "status_uspr": opusrp,
		    "status_radar": func_geral
		}
		
		print ('inicioopera')    
		status_radar_msg.send_status_radar(dado_operacionalidade)
		print ('fimopera')
		time.sleep(300)
	    
	    else:
		
		dado_operacionalidade = {
		    "radar_id": self.id_radar,
		    "status_camera": camera,
		    "status_rasp": nrf,
		    "status_uspr": opusrp,
		    "status_radar": func_geral
		}
	    
		print ('inicioopera')    
		status_radar_msg.send_status_radar(dado_operacionalidade)
		print ('fimopera')
		time.sleep(10)
	    
	   

class Cooler(object):
    def __init__(self):
	self.rele1 = 14
	GPIO.cleanup(self.rele1)
	GPIO.cleanup(15)
    	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(self.rele1, GPIO.OUT)
	
    def cooler(self):
	now = datetime.now()
	if now.hour >= 7 and now.hour <=18:
	    GPIO.output(self.rele1, GPIO.LOW)
	else:
	    GPIO.output(self.rele1, GPIO.HIGH)
	
def main():
 
    #Variáveis que compartilham Threads
    v = Queue(maxsize=0) #velocidade
    d = Queue(maxsize=0) #deteccao
    r = Queue(maxsize=0) #sinalização
    opcam = Queue(maxsize=0) #Operacionalidade câmera
    opusrp = Queue(maxsize=0) #Operacionalidade USRP 
    opnrf = Queue(maxsize=0) #Operacionalidade NRF
    cont  = Queue(maxsize=0) #Contador pra iluminação
    
    #Simplicação das Classes
    p = Processamentodesinais()
    s = Sinalizacao()
    i = Infracao()
    f = Camera()
    q = Servidor()
    w = Processamentodeimagem()
    j = Cooler()
    
    #Threads
    procsinal = threading.Thread(target = p.proc_sinal, args=(d,v))
    procsinal.setDaemon(True)
    procsinal.start()
    
    time.sleep(0.1)
    
    flag = threading.Thread(target= s.tx_rx, args = (d,r,s, cont, opnrf))
    flag.setDaemon(True)
    flag.start()
    
    time.sleep(0.1)
    
    infracao = threading.Thread(target = i.cont_infracao, args = (v, f, opcam, w, q)) 
    infracao.setDaemon(True)
    infracao.start()                                   
    
    opera = threading.Thread(target = q.operacionalidade, args = (opcam, opusrp, opnrf))
    opera.setDaemon(True)
    opera.start()

    cooler = threading.Thread(target = j.cooler, args = [])
    cooler.setDaemon(True)
    cooler.start()
    
    while True:
	pass


if __name__ == '__main__':
	       
    #Abertura da função principal
    try:	
    	main()
    except:
	GPIO.cleanup(15)
	GPIO.cleanup(14)
