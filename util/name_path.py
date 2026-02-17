from util.response import Response

from util.database import chat_collection
import json

def name_path(request, handler):
    res = Response()
    id = request.path[14:]
    user_cookie = request.cookies["session"]

    body = json.loads(request.body.decode("utf-8"))
    nickname = body["nickname"]
    chat_collection.update_many({"author": user_cookie}, {"$set": {"nickname": nickname}})
    res.text("change successful")

    handler.request.sendall(res.to_data())
