from flask import Flask
import time
import pika, ConfigParser
from optparse import OptionParser

class Connection:
	def __init__(self, connection_info=None):
		self.connection_info = connection_info
		self.credentials = pika.PlainCredentials(self.connection_info["username"], self.connection_info["password"])

        def on_response(self, ch, method, props, body):
                if self.corr_id == props.correlation_id:
                        self.response = body
                
	def send_to_queue(self, message="Hello!"):
		qname = self.connection_info["queue"]
		connection = pika.BlockingConnection(pika.ConnectionParameters(self.connection_info["server"],
									       self.connection_info["port"],'/',
									       self.credentials))
		channel = connection.channel()

		#channel.queue_declare(queue=qname)
		result = channel.queue_declare(queue=qname, exclusive=True)

                callback_queue = result.method.queue
                
                channel.basic_consume(self.on_response, no_ack=True,
                                           queue=self.callback_queue)



                self.response = None
		channel.basic_publish(exchange='',
		                     routing_key=qname,
		                     body=message)

                print(" [x] Sent %s"%message)
                
                while self.response is None:
                        time.sleep(0.2)
                        print("Waiting for response...")
                        self.connection.process_data_events()
		connection.close()
                return str(self.response)

                
app = Flask(__name__)

@app.route("/")
def index():
    return "WASPMQ Microservices\n"

@app.route("/v1/waspmq", methods=["GET"])
def waspmq():
    return "WASPMQ Microservices\n"

@app.route("/v1/waspmq/<message>")
def send(message):
	messenger.send_to_queue(message.replace("+"," "))
	return "Sent '%s'\n"%message.replace("+"," ")


if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option('-c', '--credential', dest='credentialFile',
                     help='Path to CREDENTIAL file', metavar='CREDENTIALFILE')
	(options, args) = parser.parse_args()

	if options.credentialFile:
		config = ConfigParser.RawConfigParser()
		config.read(options.credentialFile)
		connection = {}
		connection["server"] = config.get('rabbit', 'server')
		connection["port"] = int(config.get('rabbit', 'port'))
		connection["queue"] = config.get('rabbit', 'queue')
		connection["username"]=config.get('rabbit', 'username')
		connection["password"]=config.get('rabbit', 'password')

		messenger = Connection(connection_info=connection)

		#start application
		#app.run(host="0.0.0.0")
                #app.run(host="129.192.68.34",port=5555)
                app.run(host="0.0.0.0",port=5555)
	else:
        #e.g. python frontend.py -c credentials.txt
		print("Syntax: 'python frontend.py -h' | '--help' for help")


    
