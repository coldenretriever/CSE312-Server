from util.database import mongo_client
from util.response import Response
from pymongo import MongoClient
import uuid
from bson.json_util import dumps


def chat_path(request, handler):
    mongo_client = MongoClient("mongo")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    res = Response()
    if request.method == "POST":
        print("first message")
        user_cookie = str(uuid.uuid1())
        res.cookies({"session":user_cookie})
        res.text("message sent")
        chat_collection.insert_one({"messages": [{"author": user_cookie, "id": uuid.uuid1(), "content": res.body, "updated": False}]})
        print("got to chat path")

    elif request.method == "GET":
        a = True
        for key in request.cookies.keys():
            if key.__contains__("session"):
                a = False
                break
        if a:
            user_cookie = str(uuid.uuid1())
            res.cookies({"session": user_cookie})
            request.cookies["session"] = user_cookie

        user_id = request.cookies["session"]
        user_data = chat_collection.find({"author": user_id})
        res.json({"messages": [{"author": str(user_id), "id": str(uuid.uuid1()), "content": dumps(list(user_data)), "updated": False}]})

    elif request.method == "PATCH":
        id = request.path[11:]
        message = chat_collection.find({"id":id})
        if dumps(list(message)).__contains__(request.cookies["session"]):
            chat_collection.update_one({"id":id}, {'updated':True})
            chat_collection.update_one({"id":id}, {'content': request.body[13:]})


    #elif request.method == "DELETE":


    handler.request.sendall(res.to_data())
