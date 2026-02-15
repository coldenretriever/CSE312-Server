from util.database import mongo_client
from util.response import Response
from pymongo import MongoClient
import uuid
import json


def chat_path(request, handler):
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    res = Response()
    dir = "; HttpOnly"
    if request.method == "POST":
        print("first message")
        if not "session" in request.cookies.keys():
            user_cookie = str(uuid.uuid1())
        else:
            user_cookie = request.cookies["session"]
        res.cookies({"session":user_cookie + dir})
        res.text("message sent")
        body = json.loads(request.body.decode("utf-8"))
        body["content"] = body["content"].replace("&", "&amp;")
        body["content"] = body["content"].replace("<", "&lt;")
        body["content"] = body["content"].replace(">", "&gt;")

        #print(body["content"])

        print("names")
        print(db.name, chat_collection.name)
        chat_collection.insert_one({"author": user_cookie, "message_id": str(uuid.uuid1()), "content": body["content"], "updated":False})



    elif request.method == "GET":

        if not request.cookies.keys().__contains__("session"):
            user_cookie = str(uuid.uuid1())
            #res.cookies({"session": user_cookie})
            request.cookies["session"] = user_cookie

        user_id = request.cookies["session"]
        res.cookies({"session":user_id + dir})
        #print(user_id)
        message_list = []
        all_messages = chat_collection.find({})
        for d in all_messages:#user_data:
            #print(d)
            #{"messages": [{"author": string, "id": string, "content": string, "updated": boolean}, ...]}
            if "message_id" in d.keys() and "content" in d.keys() and "updated" in d.keys():
                message_list.append({"author": d["author"], "id": d["message_id"], "content": d["content"], "updated": d["updated"]})


        print(str(len(message_list)) + " length")
        res.json({"messages": message_list})

    elif request.method == "PATCH":

        #gets substring after /api/chats/
        id = request.path[11:]

        if not "session" in request.cookies.keys():
            user_id = str(uuid.uuid1())
        else:
            user_id = request.cookies["session"]
        res.cookies({"session":user_id + dir})
        entry = chat_collection.find({"message_id":id})
        for d in entry:
            if not d["author"] == user_id:
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return

        body = json.loads(request.body.decode("utf-8"))
        body["content"] = body["content"].replace("&", "&amp;")
        body["content"] = body["content"].replace("<", "&lt;")
        body["content"] = body["content"].replace(">", "&gt;")
        chat_collection.update_one({"message_id":id}, {"$set":{"content":body["content"]}})
        chat_collection.update_one({"message_id":id}, {"$set":{"updated":True}})
        res.text("change successful")


    elif request.method == "DELETE":
        #gets substring after /api/chats/
        id = request.path[11:]

        if not "session" in request.cookies.keys():
            user_id = str(uuid.uuid1())
        else:
            user_id = request.cookies["session"]
        res.cookies({"session":user_id + dir})
        user_id = request.cookies["session"]
        entry = chat_collection.find({"message_id": id})
        for d in entry:

            if not d["author"] == user_id:
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return

        chat_collection.delete_one({"message_id":id})
        res.text("deletion successful")
        print("deletion successful")
    #print("sending response")
    handler.request.sendall(res.to_data())
