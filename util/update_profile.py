import hashlib

import bcrypt

from util.auth import extract_credentials, validate_password
from util.response import Response
from util.database import user_collection

def update_profile(request, handler):
    res = Response()

    if "auth_token" not in request.cookies.keys():
        res.set_status(400, "no credentials")


    username, password = extract_credentials(request)

    users = user_collection.find({"username":username})
    count = 0
    for user in users:
        count = count + 1
    #verify that this is the only user with the specific username

    byte = password.encode('utf-8')

    hashed_auth = hashlib.sha256(request.cookies["auth_token"].encode('utf-8')).hexdigest()
    good_user = user_collection.find_one({"auth_token": hashed_auth})
    if not good_user:
        res.set_status(400, "bad credentials")
        res.json({})
        handler.request.sendall(res.to_data())
        return

    if (not validate_password(password) and password != "") or (good_user["username"] == username and count > 1):
        res.set_status(400, "invalid password")
        handler.request.sendall(res.to_data())
        return

    print("new password: " + password)
    byte = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(byte, salt)

    user_collection.update_one({"auth_token": hashed_auth},
                               {"$set": {"username": username}})
    if password != "":
        user_collection.update_one({"auth_token": hashed_auth},
                               {"$set": {"hashed": hashed_pw}})
    handler.request.sendall(res.to_data())


