from replit import web
from flask import request
import requests,os,json

def user():
    return web.auth.name

def pro_pic():
    return request.headers["X-Replit-User-Profile-Image"]

def make_dict(dictionary):
    list = dict(dictionary)
    for i in dictionary:
        list[i] = dict(dictionary[i])
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
    data = json.loads(r.text)["data"]["userByUsername"]
    return data