from flask import Flask, redirect, render_template, request, session
from dao.user_dao import UserDAO
from dao.place_dao import PlaceDAO
from dao.view_list_dao import ViewlistDAO

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
    #id = session.get("id")
    #hong
    if "id" in session:
        #session 딕셔너리 키에 hong이 있으면
        dao = UserDAO()
        id = session.get("id")
        vo = dao.get_one_user(id)
        
        region_dao = ViewlistDAO()
        region_dao.select_view_list(id)
        #최근본여행지 해야함
        
        return render_template("mypage.html", data=vo)
    else:
        return render_template("home.html")

@app.route("/logout")
def logout():
     session.pop("id", None)
     return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    q = request.form.get("q")
    # dao = PlaceDAO()
    # dao.search_places(f"%{q}%")
    return redirect(f"/board?q={q}")

@app.route("/region")
def region():
    dao = PlaceDAO()
    vo = dao.get_all_place()
    return render_template("region.html", items=vo)

@app.route("/post/<int:contentid>")
def post(contentid):
    dao = PlaceDAO()
    vo = dao.get_one_place(contentid)
    if vo:
        return render_template("post.html", data=vo)
    return redirect("/region")

@app.route("/favorite")
def favorite():
    return render_template("favorite.html")

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