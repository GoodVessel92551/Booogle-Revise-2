from replit import web
from flask import request
import requests,os,json
from better_profanity import profanity
from ai.generation import generation
from ai.moderation import moderation

def gen(prompt):
    return generation.prompt(prompt)

def mod(text):
    return moderation.prompt(text)

def username():
    return web.auth.name

def pro_pic():
    return request.headers["X-Replit-User-Profile-Image"]

def make_dict(dictionary):
    list = dict(dictionary)
    for i in dictionary:
        list[i] = dict(dictionary[i])
        for j in list[i]:
            list[i][j] = dict(dictionary[i][j])
            if "answers" in list[i][j].keys():
                list[i][j]["answers"] = dict(dictionary[i][j]["answers"])
    return list

def follow(username):
    r = requests.post("https://replit.com/graphql", json = {
      	"query": """
            query userByUsername($username: String!) {
              userByUsername(username: $username) {
                isFollowingCurrentUser
                followCount
                followerCount
                isFollowingCurrentUser
                image
            }
        }
        """,
      		"variables": """{ "username": "%s" }""" % username
    },
    headers = {
        "X-Requested-With": "ReplitApi",
        "referer": "https://replit.com/",
        "User-Agent": "Mozilla/5.0",
        "Cookie": "connect.sid="+os.getenv('sid')+""
    })
    data = json.loads(r.text)["data"]["userByUsername"]["isFollowingCurrentUser"]
    return data