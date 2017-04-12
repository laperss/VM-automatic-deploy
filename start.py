from flask import Flask
app = Flask(__name__)

CLIENTNAME = "world\n"
@app.route("/")
def index():
    '''
        Defines view for Home Page
    '''
    return "<h1>***Welcome to WASP Cloud Computing 2017!***</h1>\n"

@app.route("/v1/hello", methods=["GET"])
def hello():
    '''
        Displays a client name
    '''
    return CLIENTNAME.upper()+"\n"

@app.route("/v1/hello/<name>", methods=["GET", "POST"])
@app.route("/v1/hello/", methods=["GET", "POST"])
def update(name=None):
    '''
       Automatically update client name or display default
    '''

    if name is None:
        return hello()
    else:
        global CLIENTNAME 
        CLIENTNAME = name
        #return index()
        return "WASPY: Client name was changed. \n\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
