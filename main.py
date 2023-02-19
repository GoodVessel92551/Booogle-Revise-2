from flask import Flask, render_template,redirect,request,current_app,session
from replit import web,db
from fun import username,follow,make_dict,pro_pic,gen,mod
from better_profanity import profanity
from textblob import TextBlob
import os
user = web.UserStore()
app = Flask(__name__)
app.secret_key = os.environ['secret_key']

@app.route("/")
@web.authenticated_template("login.html")
def home():
    if username() not in db["users"]:
        db["users"].append(username())
        user.current["sets"] = {}
    return render_template("home.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),sets=make_dict(user.current["sets"]))

@app.route("/new",methods=["POST","GET"])
@web.authenticated_template("login.html")
def new():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        cover = request.form["cover"]
        if len(title) > 80 or len(title) == 0 or len(desc) > 150 or len(desc) == 0:
            session["new_set"] = {"title":title,"desc":desc,"background":cover}
            return redirect("/new")
        if title in user.current["sets"].keys():
            return redirect("/new")
        else:
            user.current["sets"][title]  = {
                "settings":{
                    "name":title,
                    "desc":desc,
                    "public":False,
                    "background":cover,
                    "user":username()
                }
            }
            session["current_set"] = title
            return redirect("/new/question")
    else:
        if session.get("new_set"):
            title = session.get("new_set")["title"]
            desc = session.get("new_set")["desc"]
            background = session.get("new_set")["background"]
            session.pop("new_set")
        else:
            title = ""
            desc = ""
            background = "animals"
        return render_template("new.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),title=title,desc=desc,background=background)

@app.route("/new/question",methods=["POST","GET"])
@web.authenticated_template("login.html")
def new_question():
    if request.method == "POST":
        quest = request.form["quest"]
        ans = request.form["ans1"]
        user.current["sets"][session.get("current_set")]["Q"+str(len(user.current["sets"][session.get("current_set")]))] = {"question":quest,"answers":{"ans1":ans}}
        try:
            ans2 = request.form["ans2"]
        except:
            pass
        else:
            try:
                user.current["sets"][session.get("current_set")]["Q"+str(len(user.current["sets"][session.get("current_set")])-1)]["answers"]["ans2"] = ans2
                ans3 = request.form["ans3"]
            except:
                pass
            else:
                user.current["sets"][session.get("current_set")]["Q"+str(len(user.current["sets"][session.get("current_set")])-1)]["answers"]["ans3"] = ans3
        if request.form["button"] == "finish":
            session.pop("current_set")
            return redirect("/")
    rude = False
    len = False
    quest = ""
    ans = ""
    if session.get("quest"):
        quests = session.get("quest")
        quest = quests["quest"]
        ans = quests["ans"]
        session.pop("quest")
    elif session.get("quest_rude"):
        rude = True
        quest = session.get("quest_rude")
        session.pop("quest_rude")
    elif session.get("quest_len"):
        len = True
        quest = session.get("quest_len")
        session.pop("quest_len")
    return render_template("new_question.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),quest=quest,ans=ans,rude=rude,len=len)

@app.route("/new/question/generate",methods=["POST","GET"])
@web.authenticated_template("login.html")
def generate():
    if request.method == "POST":
        quest = request.form["quest"]
        if len(quest.split()) < 3:
            print("len")
            session["quest_len"] = quest
        elif mod(quest) != "1" and profanity.contains_profanity(quest) == False:
            ans = gen(quest)
            session["quest"] = {"quest":quest,"ans":ans}
        else:
            session["quest_rude"] = quest
    return redirect("/new/question")

@app.route("/edit/<name>")
@web.authenticated_template("login.html")
def edit(name):
    return render_template("edit.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),sets=make_dict(user.current["sets"])[name])

@app.route("/sw.js", methods=["GET"])
def sw():
    return current_app.send_static_file("sw.js")

@app.route("/offline")
def offline():
    return render_template("offline.html")

@app.route("/flashcards/<name>")
@web.authenticated_template("login.html")
def flashcards(name):
    return render_template("cards.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),sets=make_dict(user.current["sets"])[name])

@app.route("/question")
@web.authenticated_template("login.html")
def question():
    return render_template("question.html",name=username(),boosting=follow(username()),profile_pic=pro_pic(),sets=make_dict(user.current["sets"])["set_name"])

@app.route("/delete/<name>")
@web.authenticated_template("login.html")
def delete(name):
    del user.current["sets"][name]
    return redirect("/")
    
app.run(host="0.0.0.0",port=8080,debug=True)