# -*- coding: utf-8 -*-

# module and definitions
import json
import random
import requests
import datetime

url = 'http://178.128.73.29:8080/function/figlet'
idradar = "39423"
time = datetime.datetime.utcnow()	
time = str(time.isoformat('T') + 'Z UTC-3')


vm = int(input("Velocidade medida: "))
vr = 40

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
	Infracao = "Media"
	Penalidade = "Multa"

elif vc > vinte and vc <= cinquenta:
	Infracao = "Grave"
	Penalidade = "Multa"
elif vc > cinquenta:
	Infracao = "Gravíssima"
	Penalidade = "Multa"
else:
	Infracao = "Nenhuma"
	Penalidade = "Nenhuma"

print ("Velocidade medida:",vm,"km/h" )
print ("Velocidade considerada:",vc,"km/h" )
print ("Velocidade regulamentada:",vr,"km/h")
print ("Limite 20%:",vinte,"km/h" )
print ("Limite 50%:", cinquenta,"km/h") 
print ("Infração:",Infracao)
print ("Penalidade:", Penalidade )

pacote = {
"type": "dados_carro",
	"payload": {
		"id_radar":idradar,		
		"imagem1": "base64",
		"imagem2": "base64",
		"velocidade_medida":vm,
		"velocidade_considerada":vc,
		"Velocidade_regulamentada":vr,
		"Limite_20":vinte,
		"Limite_50":cinquenta,
		"Infracao":Infracao,
		"Penalidade":Penalidade,
		"date":time
		
	}
    }
print(pacote)

def save_file():
	with open('data.json', 'w') as f:
		pacote["type"] = "dados_carro" 
		json.dump(pacote, f ,indent=2)



def send_file():   
	with open('data.json', 'r') as f: 
		r = requests.post(url, json.load(f))
		r.raise_for_status()
	return r.status_code 

save_file()
status_code = send_file()


status_code

