from flask import Flask, render_template,redirect,request,current_app
from replit import web
from fun import user,follow,make_dict,pro_pic
app = Flask(__name__)

test_app = {
    "set_name":{
        "settings":{
            "name":"name",
            "desc":"desc",
            "public":"true",
            "background":"maths",
            "user":"username",
        },
        "Q1":{
            "question":"question",
            "answers":{
                "ans1":"ans1",
            }
        },
        "Q2":{
            "question":"question",
            "answers":{
                "ans1":"ans1",
            },
        },
    },
    "set_name_1":{
        "settings":{
            "name":"name",
            "desc":"desc",
            "public":"true",
            "background":"maths",
            "user":"username",
        },
        "Q1":{
            "question":"question",
            "answers":{
                "ans1":"ans1",
            }
        },
        "Q2":{
            "question":"question",
            "answers":{
                "ans1":"ans1",
            }
        }
    }
}


@app.route("/")
@web.authenticated_template("login.html")
def home():
    return render_template("home.html",name=user(),boosting=follow(user()),profile_pic=pro_pic(),sets=test_app)

@app.route("/new")
@web.authenticated_template("login.html")
def new():
    return render_template("new.html",name=user(),boosting=follow(user()),profile_pic=pro_pic())

@app.route("/new/question")
@web.authenticated_template("login.html")
def new_question():
    return render_template("new_question.html",name=user(),boosting=follow(user()),profile_pic=pro_pic())

@app.route("/edit")
@web.authenticated_template("login.html")
def edit():
    return render_template("edit.html",name=user(),boosting=follow(user()),profile_pic=pro_pic())

@app.route("/sw.js", methods=["GET"])
def sw():
    return current_app.send_static_file("sw.js")

@app.route("/offline")
def offline():
    return render_template("offline.html")

@app.route("/flashcards")
@web.authenticated_template("login.html")
def flashcards():
    return render_template("cards.html",name=user(),boosting=follow(user()),profile_pic=pro_pic())
    
app.run(host="0.0.0.0",port=8080,debug=True)