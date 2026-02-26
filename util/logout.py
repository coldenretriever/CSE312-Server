from util.database import user_collection
from util.response import Response
from util.database import user_collection

def logout(request, handler):
    res = Response()

    # c = request.cookies
    # if "auth_token" not in c.keys():
    #     res.set_status(404, "nothing to sign out of")
    #     handler.request.sendall(res.to_data())
    #     return

    auth_token = request.cookies["auth_token"]
    print(auth_token)

    user_collection.update_one({"auth_token":auth_token}, {"$set":
                                     {"auth_token": None}})

    res.cookies({"auth_token": "deleted; HttpOnly; Max-Age=0"})
    res.set_status(302, "Found")
    res.headers({"Location":"/"})

    handler.request.sendall(res.to_data())