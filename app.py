from flask import Flask, redirect, render_template, request, session, jsonify
from dao.user_dao import UserDAO
from dao.place_dao import PlaceDAO
from vo.place_vo import PlaceVO
from dao.view_list_dao import ViewlistDAO
from dao.favorites_dao import FavoritesDAO
from dao.similar_dao import SimilarDAO

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
        #region_dao.select_view_list(id)
        #최근본여행지 해야함
        
        return render_template("mypage.html", data=vo, a="data")
    else:
        return render_template("home.html")

@app.route("/logout")
def logout():
     session.pop("id", None)
     return render_template("home.html")

@app.route("/board", methods=["GET"])
def board():
    q = request.args.get("q")
    dao = PlaceDAO()
    result = dao.search_places(q)
    return render_template("board.html", items=result)

@app.route("/region_plus", methods=["GET"])
def region_plus():
    id = session.get("id")
    page = request.args.get("page")
    regions = request.args.get("region")
    val = ", ".join(list(map(lambda x : f"\'{x}\'", regions)))
    dao = PlaceDAO()
    result = dao.get_all_place(id, val, page)
    print(page)
    response = jsonify(result=result)
    return response
    
@app.route("/region", methods=["GET"])
def region():
    dao = PlaceDAO()
    id = session.get("id")
    page = 0
    regions = request.args.getlist("region")
    val = ", ".join(list(map(lambda x : f"\'{x}\'", regions)))
    vo = dao.get_all_place(id, val, page)
    return render_template("region.html", items=vo, regions=regions)

@app.route("/post/<int:contentid>")
def post(contentid):
    dao = PlaceDAO()
    vo = dao.get_one_place(contentid)
    dao = SimilarDAO()
    svo = dao.select_similar(contentid)
    if vo or svo:
        return render_template("post.html", data=vo, similars=svo)
    return redirect("/region")

@app.route("/favorite", methods=["GET"])
def favorite():
    dao = PlaceDAO()
    id = session.get("id")
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

@app.route("/favorite_data", methods=["POST"])
def favorite_data():
    dao = FavoritesDAO()
    chInt = request.form.get("chInt")
    contentid = request.form.get("contentid")
    id = session["id"]
    print(contentid)
    print(chInt)
    if chInt == "1":
        dao.insert_favorite(id, contentid)
    else:
        dao.delete_favorite(id, contentid)
    response = jsonify(result=True)
    return response

app.run(debug=True)