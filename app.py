from flask import Flask, request, render_template
from main import parseBibTexToString as parseBibTex


app = Flask(__name__)


@app.route("/")
def my_form():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def my_form_post():
    variable = request.form["file"]
    year = request.form["year"]

    if not year:
        import datetime

        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")

    results = parseBibTex(variable, int(year))
    return render_template("results.html", results=results)
