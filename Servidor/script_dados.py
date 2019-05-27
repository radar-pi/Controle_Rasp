
# module and definitions
import json
import random
import requests

length = 1000 #Numero de casos teste
seed = 0
url = 'http://178.128.73.29:8080/function/figlet'



# demo
date = {
        'dia': "",
        'mes': "",
        'ano': "",
        'hora': "",
        'minuto': "",
        'segundo': "",
        'fuso': ""
    }
pacote = {
        "type": "dados_carro",
        "payload": {
            "imagem": "",
            "velocidade":"",
            "id_radar": "",
            'date':date
        }
    }
print(pacote)



#functions
def leap_year(year):
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))



# Data
def date_info():
    seed = 2

    fuso =  'UTC'

    ano =  random.randrange(2018,2025, seed)
    mes =    random.randrange(1, 12, seed)

    if mes == 2 and leap_year(ano) == True:
        dia =  random.randrange(0, 29, seed) 
    else :
        dia =  random.randrange(0, 28, seed)

    hora =  random.randrange(0, 24, seed)
    minuto =  random.randrange(0, 60, seed)
    segundo =  random.randrange(0, 60, seed)

    return {'fuso':fuso,'ano':ano,'mes':mes,'dia':dia,'hora':hora,'minuto':minuto,'segundo':segundo}



# file

def save_file():
    with open('data.json', 'w') as f:
        pacote['payload']['date'] = date_info()
        pacote['payload']['id_radar'] = random.randrange(0, length, 1)
        pacote['payload']['velocidade'] = random.randrange(30, 200, 1)
        pacote["type"] = "dados_carro" 
        json.dump(pacote, f ,indent=2)

def send_file():    
    with open('data.json', 'r') as f:
        r = requests.post(url, data=json.load(f))
        r.raise_for_status()
        return r.status_code 



save_file()
status_code = send_file()


status_code

