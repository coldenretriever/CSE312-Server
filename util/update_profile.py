import hashlib

import bcrypt

from util.auth import extract_credentials, validate_password
from util.response import Response
from util.database import user_collection

def update_profile(request, handler):
    res = Response()

    if "auth_token" not in request.cookies.keys():
        res.set_status(401, "no credentials")


    username, password = extract_credentials(request)

    if not validate_password(password) and password != "":
        res.set_status(401, "invalid password")
        handler.request.sendall(res.to_data())
        return

    byte = password.encode('utf-8')

    hashed_auth = hashlib.sha256(request.cookies["auth_token"].encode('utf-8')).hexdigest()
    good_user = user_collection.find_one({"auth_token": hashed_auth})
    if not good_user:
        res.set_status(401, "bad credentials")
        res.json({})
        handler.request.sendall(res.to_data())
        return


    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(byte, salt)

    user_collection.update_one({"auth_token": hashed_auth},
                               {"$set": {"username": username}})
    user_collection.update_one({"auth_token": hashed_auth},
                               {"$set": {"hashed": hashed_pw}})
    handler.request.sendall(res.to_data())


