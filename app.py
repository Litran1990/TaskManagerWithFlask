import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


"""Set up our IP address and our port number so that Cloud9 knows how to run and where to run our application"""
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
    