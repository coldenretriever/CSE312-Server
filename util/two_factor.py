import hashlib

import pyotp
import time

from util.database import user_collection
from util.response import Response


def two_factor(request, handler):
    res = Response()

    #check auth_token
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

    secret = pyotp.random_base32()
    user_collection.update_one({"auth_token": hashed}, {"$set": {"secret": secret}})
    res.json({"secret": secret})

    res.set_status(200, "found")
    handler.request.sendall(res.to_data())