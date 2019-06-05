# -*- coding: utf-8 -*-
import time
import cv2
import os
import base64
import queue
import threading
from threading import Thread
from datetime import datetime

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

def Streaming(cap):
    for i in range(2):
        ret1, frame1 = cap.read()
        ret.put(ret1)
        frame.put(frame1)
        

def File_cap(ret,frame):

    for i in range(2):
        now = datetime.now()
        hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)+':'+str(now.microsecond)
        img1 = cv2.imwrite(path+data+hora+'.jpg', frame.get())
        print("Horário Infração: ", hora)
        print("Velocidade Infração: ", vel)
        time.sleep(100)

frame = queue.Queue()
ret = queue.Queue()


while True:
    op1 = Thread(target = Streaming(cap))
    op2 = Thread(target = File_cap, args=(ret,frame))
    vel = int(input("Velocidade:"))
    if vel > 60:
        op1.start()
        op2.start()
