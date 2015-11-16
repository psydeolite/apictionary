import urllib2, json
from flask import Flask, render_template, request
import utils 

app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("/home.html")

@app.route("/result", methods=["GET"])
def result():
    query = str(request.args.get("word"))
    if (not query or
            query.isspace()):
        
        return render_template("result_page.html", query = "Invalid")

    query = query.strip()
    d = utils.define(query)

    if not d:
        error = "The word you've entered was not found. Please try your search again."
        return render_template("result_page.html", err = error, query = query)
    
    if "suggestions" in d:
        return render_template("result_page.html", pics = d, query = query)


    defins = d["definitions"]
    pics = utils.pictify(d)
    return render_template("/result_page.html", query=query, defins=defins, pics=pics)




if __name__ == "__main__":
    app.debug = True
    app.secret_key = "69cce1c1daa03989"
    app.run(host = '0.0.0.0', port = 8000)
