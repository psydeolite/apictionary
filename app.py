import urllib2, json
from flask import Flask, render_template, request
import utils 

app = Flask(__name__)

@app.route("/t")
@app.route("/t/<tag>")
def t(tag = "rose cut"):
    urls = utils.pictify(tag)
    return render_template("results.html", urls = urls)
    



if __name__ == "__main__":
    app.debug = True
    app.secret_key = "69cce1c1daa03989"
    app.run(host = '0.0.0.0', port = 8000)
