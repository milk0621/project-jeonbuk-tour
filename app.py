from flask import Flask, redirect, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/region")
def region():
    return render_template("region.html")

@app.route("/theme")
def theme():
    return render_template("theme.html")

app.run(debug=True)