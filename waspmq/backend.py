#!/usr/bin/env python
import time
import pika
from optparse import OptionParser
import ConfigParser


def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

def receive(connection_info=None):
        qname = connection_info["queue"]
        credentials = pika.PlainCredentials(connection_info["username"], connection_info["password"])
        connection = pika.BlockingConnection(pika.ConnectionParameters(connection_info["server"],connection_info["port"],'/',credentials))
        channel = connection.channel()
        channel.queue_declare(queue=qname)
        #channel.basic_consume(callback, queue=qname, no_ack=True)
        channel.basic_consume(on_request, queue=qname, no_ack=True)
        channel.basic_qos(prefetch_count=1)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


def on_request(ch, method, props, body):
        string = str(body)
        print(" [.] convert video %s" %string)
        time.sleep(3)
        response = string
        print("routing key:")
        print(props.reply_to)
        print("------------")
        
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
if __name__=="__main__":
        parser = OptionParser()
        parser.add_option('-c', '--credential', dest='credentialFile', help='Path to CREDENTIAL file', metavar='CREDENTIALFILE')
        (options, args) = parser.parse_args()

        if options.credentialFile:
                config = ConfigParser.RawConfigParser()
                config.read(options.credentialFile)
                connection = {}
                connection["server"] = config.get('rabbit', 'server')
                connection["port"] = int(config.get('rabbit', 'port'))
                connection["queue"] = config.get('rabbit', 'queue')
                connection["username"] = config.get('rabbit', 'username')
                connection["password"] = config.get('rabbit', 'password')
                receive(connection_info=connection)
        else:
                print("Syntax: 'python backend.py -h' | '--help' for help")

