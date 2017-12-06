#!/usr/bin/env python3
import os, shlex, random, string, binascii, shutil, sys, time, uuid
import subprocess
from flask import Flask, request, redirect, url_for, render_template, send_file, session, after_this_request
from subprocess import DEVNULL, STDOUT, call
import pika, configparser
from optparse import OptionParser
import json
from base64 import b64encode, b64decode, decodestring

# The allowed video extensions for conversion
ALLOWED_EXTENSIONS = set(['mkv', 'mp4'])

IP_ADDRESS = subprocess.check_output("ifconfig | grep  -m1 'inet addr:' | cut -d: -f2 | awk '{ print $1}'", shell=True)

print("Look for IP address of queue...")
QUEUE_ADDRESS = subprocess.check_output("python3 /home/ubuntu/VM-automatic-deploy/vmanager.py --action show-ip waspmq", shell=True).decode('utf-8')
print("RabbitMQ address: ", QUEUE_ADDRESS)

class Connection:
    def __init__(self, connection_info=None):
        self.connection_info = connection_info
        self.credentials = pika.PlainCredentials(self.connection_info["username"], self.connection_info["password"])

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')
            print("File recieved")
            try:
                response_dict = json.loads(self.response)
                output_path = response_dict['output_path']
                hostname = response_dict['hostname'].replace('-', '_')
                session['filename'] = response_dict['filename'].strip()
                session['ip'] = response_dict['ip_address'].strip()
                input_path_tmp = response_dict['input_path']
                print("Download file locally from ", session['ip'])
                session['input_path'] = response_dict['input_path']
                os.system("scp -i /home/ubuntu/vm-key.pem" + " ubuntu@" + session["ip"] + ":"
                          + input_path_tmp + " " + output_path +  " > /dev/null")
                #command = ('ssh -i /home/ubuntu/vm-key.pem ubuntu@' + session["ip"] +
                #           ' "sudo rm ' + input_path_tmp + '"')
                #host = 'ubuntu@' + session['ip']
                #print(command)
                #print(host)
                #subprocess.Popen(["ssh", "%s" % host, command],
                #                 shell=False,
                #                 stdout=subprocess.PIPE,
                #                 stderr=subprocess.PIPE)

                print("Download complete")
            except:
                output_path = self.response

            input_path = output_path.replace("output", "input")
            try:
                os.remove(input_path)
            except:
                pass

            session['output_path'] = output_path
            
    def send_to_queue(self, message="Hello!"):
        qname = self.connection_info["queue"]
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.connection_info["server"],
                                                                       self.connection_info["port"],'/',
                                                                       self.credentials))
        channel = connection.channel()
        result = channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        channel.basic_consume(self.on_response, no_ack=True,
                              queue=callback_queue)
        # Send message
        self.corr_id = str(uuid.uuid4())
        print("ID: ", self.corr_id)
        channel.basic_publish(exchange='', routing_key=qname,
                              properties=pika.BasicProperties(reply_to=callback_queue,
                                                              correlation_id=self.corr_id),
                              body=message)
        print(" [x] Sent video to RabbitMQ'")
        self.response = None
        # Wait for response
        while self.response is None:
            connection.process_data_events()
        connection.close()
        return str(self.response)



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/tmp'
app.config['SECRET_KEY'] =  binascii.hexlify(os.urandom(24))

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        print("request.method == POST")
        print(request.files)
        input_ = request.files['upload_file']
        filename, input_ext = os.path.splitext(input_.filename)
        print(filename)
        if input_ and allowed_file(input_.filename):
            random_str = random_string()
            input_file = "input_%s.mkv" % (random_str)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
            input_.save(input_path)
            string = ("Trying to send video '%s' to rabbitmq" %filename)
            messenger.send_to_queue(input_path)
            return redirect(url_for('done'))
    return render_template('upload.html')
    

@app.route("/done", methods=['GET'])
def done():
    return render_template('done.html')

@app.route("/download_file", methods=['GET'])
def download_file():
    output_path = session['output_path']
    print("Download request: ", output_path)
    if 'hostname' in session.keys():
        hostname = session['hostname']
        print("Download from host: ", hostname )

    _, output_ext = os.path.splitext(output_path)
    output_handle = open(output_path, 'r')
    @after_this_request
    def remove_file(response):
        try:
            os.remove(output_path)
            output_handle.close()
        except Exception as error:
            app.logger.error("Error removing the output file: ", error)
        return response
    
    return send_file(output_path,  attachment_filename='converted_file%s' % output_ext, as_attachment=True)

if __name__ == "__main__":
    # Connect to rabbitmq
    parser = OptionParser()
    parser.add_option('-c', '--credential', dest='credentialFile',
                      help='Path to CREDENTIAL file', metavar='CREDENTIALFILE')
    (options, args) = parser.parse_args()
    if options.credentialFile:
        config = configparser.RawConfigParser()
        config.read(options.credentialFile)
        connection = {}
        connection["server"] = QUEUE_ADDRESS
        connection["port"] = int(config.get('rabbit', 'port'))
        connection["queue"] = config.get('rabbit', 'queue')
        connection["username"]=config.get('rabbit', 'username')
        connection["password"]=config.get('rabbit', 'password')
        messenger = Connection(connection_info=connection)
    else:
        print("No credentials file was given")

    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
