import time
import cv2
import os
import base64
from datetime import datetime

##inicializando
path = 'Banco_de_Imagens/'
now = datetime.now()
data = str(now.day)+'_'+str(now.month)+'_'+str(now.year)+'/'
dirfailed = 512# caso nao consiga criar diretorio
cap = cv2.VideoCapture('rtsp://admin:radarpi2@10.0.0.100:554') # it can be rtsp or http stream

ret, frame = cap.read()

if os.system('cd '+ path + data) == dirfailed:
    os.system('mkdir '+ path + data)
    os.system('cd '+ path + data)
control = 'r'
i=0
while True:#control != "q":
    #control = input('Comando: ')
    #if control == "n":
    i = i+1;
    inicio = time.time()
    if cap.isOpened():
        _,frame = cap.read()
        
        if _ and frame is not None:
            now = datetime.now()
            hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)+':'+str(now.microsecond)
            img1 = cv2.imwrite(path+data+hora+'.jpg', frame)
            fim = time.time()
            print (hora)
            print(fim - inicio)
            print(i)
            time.sleep(0.1)
            
            
cap.release() #releasing camera immediately after capturing picture


   
    
    



#with open ("/home/pi/Documents/teste4.jpg","rb") as file:
#    IMG = base64.b64encode(file.read())

# Fim do programa

#-----------------------------------------------------
#if __name__ == '__main__':
#    main() # chamada que inicia o programa
