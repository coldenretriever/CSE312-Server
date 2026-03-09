import hashlib
import uuid

from util.database import user_collection
from util.response import Response


def github_session(login, handler):
    res = Response()
    #register
    user_collection.insert_one({"username": login,
                                "id": str(uuid.uuid4()),
                                "hashed": "",
                                "auth_token": None})

    #login
    auth_string = str(uuid.uuid4())
    res.cookies({"auth_token": auth_string + "; HttpOnly; Max-Age=3600"})
    auth_token = auth_string.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(auth_token)
    auth_hash = sha256.hexdigest()
    user_collection.update_one({"username": login}, {"$set":
                                                            {"auth_token": auth_hash}})

    res.text("logged in with github")
    handler.request.sendall(res.to_data())