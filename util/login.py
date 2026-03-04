import hashlib
import uuid

import bcrypt
import pyotp

from util.auth import extract_credentials, validate_password
from util.response import Response
from util.database import user_collection

def login(request, handler):
    res = Response()

    username, password, totp = extract_credentials(request)

    byte = password.encode('utf-8')
    hashed = user_collection.find_one({"username":username})["hashed"]

    if not hashed or not bcrypt.checkpw(byte, hashed):
        res.set_status(400, "incorrect pw")
        res.text("bad pw bad")
        handler.request.sendall(res.to_data())
        return

    entry = user_collection.find_one({"username": username})
    if entry.keys().__contains__("secret") and totp == "":
        res.set_status(401, "no totp sent")
        res.text("no totp sent")
        handler.request.sendall(res.to_data())
        return
    elif entry.keys().__contains__("secret") and totp != "":
        current = pyotp.TOTP(entry["secret"])
        if not current.verify(totp):
            res.set_status(401, "no totp sent")
            res.text("totp invalid")
            handler.request.sendall(res.to_data())
            return

    auth_string = str(uuid.uuid4())
    res.cookies({"auth_token": auth_string + "; HttpOnly; Max-Age=3600"})
    auth_token = auth_string.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(auth_token)
    auth_hash = sha256.hexdigest()
    user_collection.update_one({"username":username}, {"$set":
                                     {"auth_token": auth_hash}})


    res.text("reg/login successful")
    handler.request.sendall(res.to_data())







