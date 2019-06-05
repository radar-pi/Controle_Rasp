# -*- coding: utf-8 -*-

# module and definitions
import json
import random
import requests
import datetime
import base64
import time
import os
from controle_infracao import controle_infra
for i in range(5):
	print('\n')
	url = "http://178.128.73.29:8080/function/cows"
	inicio = time.time()
	def save_file(pacote):
	    with open('data.json', 'w') as f:
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
		camera = random.randrange(0,2)
		raspberry = random.randrange(0,2)
		usrp = random.randrange(0,2)
		func_geral = random.randrange(0,2)
		time = datetime.datetime.utcnow()
		time = str(time.isoformat('T') + 'Z')
		with open("21:45:1:884238.jpg", "rb") as file:
			img1 = base64.b64encode(file.read())
		with open("21:45:1:884238.jpg", "rb") as file:
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
		        "date":time,
			"camera": camera,
			"raspberry": raspberry,
			"usrp": usrp,
			"func_geral": func_geral
		    }
		}

		pacote.append(base)
		base = {}
	    
	    save_file(pacote)
	    x = send_file(url)
	    print('Codigo de Estado:', x)

	 
	#send não está sendo chamada.
	main()
	fim = time.time()
	print('Tempo de envio:', fim-inicio)
	tamanho = os.path.getsize ('data.json')
	print('Tamanho do pacote:', tamanho)

