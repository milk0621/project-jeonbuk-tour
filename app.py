from flask import Flask, redirect, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("header.html")

app.run(debug=True)