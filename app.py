from flask import Flask, redirect, render_template, request
from dao.user_dao import UserDAO
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
        

@app.route("/join", methods=["POST"])
def join():
    id = request.form.get("id")
    pw = request.form.get("pw")
    name = request.form.get("name")
    email = request.form.get("email")
    dao = UserDAO()
    dao.join(id, pw, name, email)
    return redirect("/")


@app.route("/region")
def region():
    return render_template("region.html")

@app.route("/theme")
def theme():
    return render_template("theme.html")

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/course")
def recommend():
    return render_template("course.html")

app.run(debug=True)