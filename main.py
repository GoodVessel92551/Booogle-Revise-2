from flask import Flask, render_template,redirect,request
from replit import web
from fun import user,follow,make_dict,pro_pic
app = Flask(__name__)


@app.route("/")
@web.authenticated_template("login.html")
def home():
    return render_template("home.html",name=user(),boosting=follow(user()),profile_pic=pro_pic())


app.run(host="0.0.0.0",port=8080,debug=True)