import hashlib

from util.database import user_collection
from util.response import Response


def at_me(request, handler):
    res = Response()
    if "auth_token" not in request.cookies:
        res.set_status(401, "not logged in")
        res.json({})
        handler.request.sendall(res.to_data())
        return

    hashed = hashlib.sha256(request.cookies["auth_token"].encode('utf-8')).hexdigest()
    good_user = user_collection.find_one({"auth_token": hashed})
    if not good_user:
        res.set_status(401, "bad credentials")
        res.json({})
        handler.request.sendall(res.to_data())
        return

    body = {}
    for k in good_user:
        print(k)
        if k != "_id" and k != "hashed" and k != "auth_token":
            body[k] = good_user[k]
    print(body)
    res.json(body)
    handler.request.sendall(res.to_data())

