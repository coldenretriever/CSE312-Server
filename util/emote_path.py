from util.response import Response

from util.database import chat_collection
import json

def emote_path(request, handler):
    res = Response()
    if request.method == "PATCH":
        # gets substring after /api/reaction/
        #dictionary of emoji to user_ids
        id = request.path[14:]
        print(id)
        body = json.loads(request.body.decode("utf-8"))
        emoji = body["emoji"]
        entry = chat_collection.find({"message_id": id})

        user_cookie = request.cookies["session"]

        # reactions : {emoji : user_id}

        for d in entry:
            if emoji not in d["reactions"]:
               reactions = {}
            else:
               reactions = d["reactions"]
            print("place")
            print(d["reactions"])
            print(reactions)
            if emoji in d["reactions"].keys() and d["reactions"][emoji].__contains__(user_cookie):
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return
            #if the emoji isn't there yet
            if emoji not in d["reactions"].keys():
                reactions[emoji] = [user_cookie]
            else:
                reactions[emoji] = reactions[emoji].append(user_cookie)
            chat_collection.update_one({"message_id": id}, {"$set": {"reactions": reactions}})

        res.text("change successful")
    elif request.method == "DELETE":
        id = request.path[14:]
        body = json.loads(request.body.decode("utf-8"))
        emoji = body["emoji"]
        entry = chat_collection.find({"message_id": id})
        for d in entry:
            reactions = entry["reactions"]
            if not d["emoji"].__contains__(emoji):
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return
            reactions.append(emoji)
            chat_collection.delete({"message_id": id})

        res.text("delete successful")

    handler.request.sendall(res.to_data())
