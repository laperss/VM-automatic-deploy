from __future__ import print_function
import time
import string
import random
import pika
import configparser
import vmanager


BACKEND_SCRIPT = 'waspmq/backend.sh'
FRONTEND_SCRIPT = 'waspmq/backend.sh'
RABBITMQ_SCRIPT = 'waspmq/waspmq.sh'

NETWORK = 'sw_network'

manager = vmanager.Manager()

QUEUE_ADDRESS = manager.get_IP('waspmq')

print("QUEUE IP: ", QUEUE_ADDRESS)

config = configparser.RawConfigParser()
config.read('waspmq/credentials.txt')
connection_info = {}
connection_info["server"] = QUEUE_ADDRESS
connection_info["port"] = int(config.get('rabbit', 'port'))
connection_info["queue"] = config.get('rabbit', 'queue')
connection_info["username"]=config.get('rabbit', 'username')
connection_info["password"]=config.get('rabbit', 'password')

print("* Connect to queue")
credentials = pika.PlainCredentials(connection_info["username"], connection_info["password"])
params = pika.ConnectionParameters(connection_info["server"],connection_info["port"],'/', credentials)
connection = pika.BlockingConnection(parameters=params)
print("* Connection succeeded: ", connection.is_open)

channel = connection.channel()
channel.queue_delete(queue='video-queue')
