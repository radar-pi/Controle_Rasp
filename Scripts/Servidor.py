# -*- coding: utf-8 -*-

# module and definitions
import json
import random
import requests
import datetime
import base64
from controle_infracao import controle_infra

def save_file(pacote):
    with open('data.json', 'a') as f:
        json.dump(pacote, f ,indent=2)

def send_file(url):   
	with open('data.json', 'r') as f: 
		r = requests.post(url, json.load(f))
		r.raise_for_status()
	return r.status_code 

def main():
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

        lista = controle_infra()
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
    
    save_file(pacote)

#send não está sendo chamada.
main()
