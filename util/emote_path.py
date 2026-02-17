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
            reactions = d["reactions"]
            print("place")
            print(d["reactions"])
            print(reactions)
            print(d["reactions"].keys())
            if emoji in d["reactions"].keys() and d["reactions"][emoji].__contains__(user_cookie):
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return
            #if the emoji isn't there yet
            print("two")
            if emoji not in d["reactions"].keys():
                print(reactions)
                reactions[emoji] = [user_cookie]
                print(reactions)
                print("took 1")
            else:
                print("before add")
                l = reactions[emoji]
                l.append(user_cookie)
                reactions[emoji] = l
                print("after add")
                print("took 2")
            print("three")
            print(reactions)
            chat_collection.update_one({"message_id": id}, {"$set": {"reactions": reactions}})

        res.text("change successful")
    elif request.method == "DELETE":
        user_cookie = request.cookies["session"]
        id = request.path[14:]
        body = json.loads(request.body.decode("utf-8"))
        emoji = body["emoji"]
        entry = chat_collection.find({"message_id": id})
        for d in entry:
            reactions = d["reactions"]
            print(reactions)
            if user_cookie not in reactions[emoji]:
                print("wrong delete")
                print(user_cookie)
                print(reactions[emoji])
                print("403 FORBIDDEN")
                res.set_status(403, "Forbidden")
                res.text("forbidden access")
                handler.request.sendall(res.to_data())
                return

            l = reactions[emoji]
            if len(l) == 1:
                reactions.pop(emoji)
            else:
                l.remove(user_cookie)
                reactions[emoji] = l
            #need to properly remove 1 user_cookie
            chat_collection.update_one({"message_id": id}, {"$set": {"reactions": reactions}})


            #chat_collection.delete({"message_id": id})

        res.text("delete successful")

    handler.request.sendall(res.to_data())
