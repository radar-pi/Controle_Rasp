
# module and definitions
import json
import random
import requests
import datetime

url = 'http://178.128.73.29:8080/function/figlet'
vel = 60
idradar = "39423"
time = datetime.datetime.utcnow()	
time = str(time.isoformat('T') + 'Z UTC-3')
print(time)


# demo

pacote = {
"type": "dados_carro",
	"payload": {
		"imagem1": "base64",
		"imagem2": "base64",
		"velocidade":vel,
		"id_radar":idradar,
		"date":time
	}
    }
print(pacote)


def send_file():    
        r = requests.post(url, data=pacote)
        r.raise_for_status()
        return r.status_code 

status_code = send_file()


status_code

