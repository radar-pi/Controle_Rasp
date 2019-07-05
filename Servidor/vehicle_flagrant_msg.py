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

print '5'
def _generate_id():
    identifier = str(uuid.uuid4())
    return identifier


def _get_time():
    time = datetime.datetime.utcnow()
    time = str(time.isoformat('T') + 'Z')
    return time
print '10'

def send_vehicle_flagrant(dict_msg=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    main_channel = connection.channel()

    main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
    print '15'
    msg = {
        "type": "vehicle-flagrant",
        "id": _generate_id(),
        "time": _get_time(),
        "payload": {
            "id_radar": dict_msg['id_radar'],
            "image1": dict_msg['image1'],
            "image2": dict_msg['image2'],
            "infraction": dict_msg['infraction'],
            "vehicle_speed": dict_msg['vehicle_speed'],
            "considered_speed": dict_msg['considered_speed'],
            "max_allowed_speed": dict_msg['max_allowed_speed']
        }
    }
    
    main_channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=json.dumps(msg),
        properties=pika.BasicProperties(content_type='application/json'))
    #print('send message %s' % msg)
    print 'ok'
    connection.close()
