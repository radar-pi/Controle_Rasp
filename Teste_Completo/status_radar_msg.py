# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import json
import pika
import sys
import uuid
import datetime

EXCHANGE = 'message'
EXCHANGE_TYPE = 'topic'
QUEUE = 'maestro'
ROUTING_KEY = 'message.maestro'
HOST = 'www.radop.ml'


def _generate_id():
    identifier = str(uuid.uuid4())
    return identifier


def _get_time():
    time = datetime.datetime.utcnow()
    time = str(time.isoformat('T') + 'Z')
    return time


def send_status_radar(dict_msg=None):
    #print('DEBUG iniciando o envio da mensagem')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    main_channel = connection.channel()

    main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

    msg = {
        "id": _generate_id(),
        "type": "status-radar",
        "payload": {
            "radar_id": dict_msg['radar_id'],
            "radar": dict_msg['status_radar'],
            "camera": dict_msg['status_camera'],
            "rasp": dict_msg['status_rasp'],
            "usrp": dict_msg['status_uspr']
        },
        "time": _get_time()
    }
    
    #print('DEBUG preparando para enviar a mensagem')
    main_channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=json.dumps(msg),
        properties=pika.BasicProperties(content_type='application/json'))
    print('send message %s' % msg)

    connection.close()
