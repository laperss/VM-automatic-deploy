#!/usr/bin/env python3
import os, shlex, random, string, binascii, shutil, sys, time, uuid
from flask import Flask, request, redirect, url_for, render_template, send_file, session

from subprocess import DEVNULL, STDOUT, call
import pika, configparser
from optparse import OptionParser
import json
from base64 import b64encode, b64decode, decodestring

class Connection:
    def __init__(self, connection_info=None):
        self.connection_info = connection_info
        self.credentials = pika.PlainCredentials(self.connection_info["username"], self.connection_info["password"])

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            print("File recieved")
            self.response = body.decode('utf-8')
            jsonToPython = json.loads(self.response)
            videoString = jsonToPython[u'video']['video']
            video = b64decode(videoString)
            
            random_str = random_string()
            output_file = "output_%s.mkv" % (random_str)
            
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file)
            f = open(output_path, 'wb')
            f.write(video)
            f.close()
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
        channel.basic_publish(exchange='', routing_key=qname,
                              properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=self.corr_id),
                              body=message)
        print(" [x] Sent video to RabbitMQ'")
        self.response = None
        # Wait for response
        while self.response is None:
            #time.sleep(0.5)
            #print("Waiting for response...")
            connection.process_data_events()
        connection.close()
        return str(self.response)


ALLOWED_EXTENSIONS = set(['mkv', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tmp'
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
        input_ = request.files['file']
        filename, input_ext = os.path.splitext(input_.filename)
        print(filename)
        if input_ and allowed_file(input_.filename):
            # Saving input file
            string = ("Trying to send video '%s' to rabbitmq" %filename)
            random_str = random_string()
            input_file = "input_%s.mkv" % (random_str)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
            input_.save(input_path)
            print("[local]\tSaving input file " + input_file + "...")

            # Publish task to all workers
            taskid = random.randint(0, 100)
            task = "task " + str(taskid)

            with open(input_path, 'rb') as f:
                contents = f.read()
                base64_bytes = b64encode(contents)
                base64_string = base64_bytes.decode('utf-8')
                raw_data = base64_string

            pythonDictionary = {'filename':filename, 'video':raw_data, 'taskID':taskid}
            dictionaryToJson = json.dumps(pythonDictionary)
            messenger.send_to_queue(dictionaryToJson)

            # Delete input file
            print("[local]\tDeleting input file " + input_file + "...")
            os.remove(input_path)

            return redirect(url_for('done'))
    return render_template('upload.html')
    

@app.route("/done", methods=['GET'])
def done():
    return render_template('done.html')

@app.route("/download_file", methods=['GET'])
def download_file():
    output_path = session['output_path']
    _, output_ext = os.path.splitext(output_path)
    return send_file(output_path,  attachment_filename='converted_file%s' % output_ext, as_attachment=True)

if __name__ == "__main__":
    # CONNECT TO BACKEND VIA RABBITMQ VM
    parser = OptionParser()
    parser.add_option('-c', '--credential', dest='credentialFile',
                      help='Path to CREDENTIAL file', metavar='CREDENTIALFILE')
    (options, args) = parser.parse_args()
    if options.credentialFile:
        config = configparser.RawConfigParser()
        config.read(options.credentialFile)
        connection = {}
        connection["server"] = config.get('rabbit', 'server')
        connection["port"] = int(config.get('rabbit', 'port'))
        connection["queue"] = config.get('rabbit', 'queue')
        connection["username"]=config.get('rabbit', 'username')
        connection["password"]=config.get('rabbit', 'password')
        messenger = Connection(connection_info=connection)
    # RUN APPLICATION ONLINE
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
