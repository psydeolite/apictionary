import urllib2, json
from flask import Flask, render_template, request
import utils 

app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=["GET"])
def home():
    return render_template("/home.html")

@app.route("/result")
def result():
    return render_template("/result_page.html")




if __name__ == "__main__":
    app.debug = True
    app.secret_key = "69cce1c1daa03989"
    app.run(host = '0.0.0.0', port = 8000)
