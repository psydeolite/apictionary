import urllib2, json
from flask import Flask, render_template, request
import utils 

app = Flask(__name__)





if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
