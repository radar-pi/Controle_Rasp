# -*- coding: utf-8 -*-

# module and definitions
import json
import random
import requests
import datetime
import random
import 
url = 'http://178.128.73.29:8080/function/figlet'
idradar = random.randrange(0,10)
time = datetime.datetime.utcnow()	
time = str(time.isoformat('T') + 'Z')


vm = int(random.randrange(20,150))
vr = int(random.randrange(40,80,20))

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
	vc = vminfracao


vinte = int (vr + ((20*40)/100))	
cinquenta = vr + ((50*40)/100)

if  vc >= vr and vc <= vinte:
	infracao = 1
	penalidade = True

elif vc > vinte and vc <= cinquenta:
	infracao = 2
	penalidade = True
elif vc > cinquenta:
	infracao = 3
	penalidade = True
else:
	infracao = 0
	penalidade = False

print ("Velocidade medida:",vm,"km/h" )
print ("Velocidade considerada:",vc,"km/h" )
print ("Velocidade regulamentada:",vr,"km/h")
print ("Limite 20%:",vinte,"km/h" )
print ("Limite 50%:", cinquenta,"km/h") 
print ("Infração:",infracao)
print ("penalidade:", penalidade )

pacote = {
"type": "dados_carro",
	"payload": {
		"id_radar":idradar,
		"infracao":infracao, #enumeracao  nenhuma ->0 media ->1 grave ->2 gravíssima ->3		
		"imagem1": "base64",
		"imagem2": "base64",
		"velocidade_medida":vm,#int
		"velocidade_considerada":vc,#int
		"velocidade_regulamentada":vr,# int
		"penalidade":penalidade,#boolean
		"date":time
	}
    }
print(pacote)

def save_file():
	with open('data.json', 'a') as f:
		pacote["type"] = "dados_carro" 
		json.dump(pacote, f ,indent=2)



def send_file():   
	with open('data.json', 'r') as f: 
		r = requests.post(url, json.load(f))
		r.raise_for_status()
	return r.status_code 
	
for i in range(100):
	save_file()
#status_code = send_file()


#status_code

