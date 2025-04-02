from flask import Flask, redirect, render_template, request, session
from dao.user_dao import UserDAO
from dao.place_dao import PlaceDao
app = Flask(__name__)
app.secret_key = "***REMOVED***"

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

@app.route("/login", methods=["POST"])
def login():
    id = request.form.get("id")
    pw = request.form.get("pw")
    dao = UserDAO()
    result = dao.login(id, pw)
    if result:
        session["id"] = id
    return redirect("/")

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")

@app.route("/search", methods=["POST"])
def search():
    q = request.form.get("q")
    dao = PlaceDao()
    dao.search_places(q)
    return redirect(f"/board?q={q}")

@app.route("/region")
def region():
    dao = PlaceDao()
    vo = dao.get_all_place()
    return render_template("region.html", items=vo)

@app.route("/post/<int:contentid>")
def post(no):
    dao = PlaceDao()
    vo = dao.get_one_place(no)
    if vo:
        return render_template("post.html", data=vo)
    return redirect("/region")

@app.route("/theme")
def theme():
    return render_template("theme.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/course")
def recommend():
    return render_template("course.html")

app.run(debug=True)