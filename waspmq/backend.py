#!/usr/bin/env python 
import time
import pika
from optparse import OptionParser
import ConfigParser
import base64 
import string
import os

def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


def convert_video(source, dest):
        cmd = "mencoder %s -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=3000 -oac copy -o %s >/dev/null 2>&1" % (source, dest)
        os.system(cmd)

def receive(connection_info=None):
        qname = connection_info["queue"]
        print("qname: ", qname)
        credentials = pika.PlainCredentials(connection_info["username"], connection_info["password"])
        connection = pika.BlockingConnection(pika.ConnectionParameters(connection_info["server"],connection_info["port"],'/',credentials))
        channel = connection.channel()
        channel.queue_declare(queue=qname)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue=qname)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

def on_request(ch, method, props, body):
        input_path = body #jsonToPython[u'input_path']
        [_, filename] = os.path.split(input_path)
        output_path = '/home/ubuntu/tmp/output_' + filename

        input_file_tmp =  '/home/ubuntu/tmp/' + filename
        output_file_tmp =  '/home/ubuntu/tmp/output_' + filename

        # Transfer video file
        os.system("scp -i /home/ubuntu/vm-key.pem " + " ubuntu@" + MASTER_IP + ":" + input_path + " " + input_file_tmp +  " > /dev/null")

        # filename, input_ext = os.path.splitext(filename)

        print(" [.] Starting conversion... ")
        convert_video(input_file_tmp, output_file_tmp)
        os.remove(input_file_tmp)
        print(" [.] Conversion finished." )

        os.system("scp -i /home/ubuntu/vm-key.pem " +  output_file_tmp + " ubuntu@" + MASTER_IP + ":" + output_path + " > /dev/null")
        os.remove(output_file_tmp)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=output_path)
        
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
          
if __name__=="__main__":
        # CONNECT TO RABBITMQ TO RECIEVE FROM FRONTEND
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
