import bcrypt

from util.auth import extract_credentials, validate_password
from util.response import Response
from util.database import user_collection


def register(request, handler):
    res = Response()
    path = request.path

    username, password = extract_credentials(request)


    if not validate_password(password) or user_collection.find_one({"username": username}):
        res.set_status(400, "bad password")
        res.text("denied")
        handler.request.sendall(res.to_data())
        return


    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte, salt)

    user_collection.insert_one({"username":username,
                                "hashed": hashed,
                                "auth_token": None})

    res.text("reg/login successful")

    handler.request.sendall(res.to_data())







