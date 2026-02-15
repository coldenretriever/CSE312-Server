from util.database import mongo_client
from util.response import Response
from pymongo import MongoClient
import uuid
import json


def chat_path(request, handler):
    mongo_client = MongoClient("mongo")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    res = Response()
    if request.method == "POST":
        print("first message")
        if not "session" in request.cookies.keys():
            print("making new cookie")
            user_cookie = str(uuid.uuid1())
        else:
            user_cookie = request.cookies["session"]
        res.cookies({"session":user_cookie})
        res.text("message sent")

        body = json.loads(request.body.decode("utf-8"))
        body["content"] = body["content"].replace("&", "&amp")
        body["content"] = body["content"].replace("<", "&lt")
        body["content"] = body["content"].replace(">", "&gt")
        message_id = str(uuid.uuid4())
        chat_collection.insert_one({"author": user_cookie, "message_id": message_id, "content": body["content"]})
        a = chat_collection.find({})
        for d in a:
            print(d)
            print("//////////")
        print("made it")

    elif request.method == "GET":


        message_list = []
        all_messages = chat_collection.find({})
        for d in all_messages:
            print(str(d) + "||||||||||||||||")
            if not "message_id" in d.keys():
                print("not in keys")
            #{"messages": [{"author": string, "id": string, "content": string, "updated": boolean}, ...]}
            message_list.append({"author": d["author"], "id": d["message_id"], "content":d["content"], "updated": False})

            res.json({"messages": message_list})

    elif request.method == "PATCH":
        #should I have situation for
        #  -someone accesses without cookie
        #  -
        print(request.path)
        id = request.path[11:]
        print(id)

        user_id = request.cookies["session"]
        entry = chat_collection.find({"message_id":id})
        for d in entry:
            if not user_id in d.keys():
                res.set_status(403, "Forbidden")
                handler.request.sendall(res.to_data())

        body = json.loads(request.body)
        body["content"] = body["content"].replace("&", '&amp')
        body["content"] = body["content"].replace("<", "&lt")
        body["content"] = body["content"].replace(">", "&gt")
        chat_collection.update_one({"message_id":id}, {"$set":{"content":body["content"]}})
        chat_collection.update_one({"message_id":id}, {"$set":{"updated":True}})
        res.text("change successful")
        #correctly format this

    elif request.method == "DELETE":
        id = request.path[11:]

        user_id = request.cookies["session"]
        entry = chat_collection.find({"message_id": id})
        a = True
        for d in entry:
            print("got entry")
            if d["author"] == user_id:
                a = False
        if a:
            print("sent 403")
            res.set_status(403, "Forbidden")
            handler.request.sendall(res.to_data())

        chat_collection.delete_one({"message_id":id})
        print("deleted successfully")
        res.text("deletion successful")
    #print("sending response")
    handler.request.sendall(res.to_data())

