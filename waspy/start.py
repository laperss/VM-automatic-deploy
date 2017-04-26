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

if __name__ == "__main__":
    app.run(host="0.0.0.0")
