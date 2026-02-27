from util.database import user_collection
from util.response import Response


def search(request, handler):
    res = Response()
    output = {"users": []}
    path = request.path
    if "user" not in path:
        res.set_status(404, "nothing there")
        handler.request.sendall(res.to_data())
        return

    print(path)
    print("above")
    before, query = path.split("=", 1)

    if query == "":
        res.set_status(404, "nothing there")
        handler.request.sendall(res.to_data())
        return

    entries = user_collection.find({})
    for entry in entries:
        if "username" in entry.keys():
            if entry["username"].startswith(query):
                cur = output["users"]
                cur.append({"id":entry["id"], "username":entry["username"]})
                output["users"] = cur
    res.json(output)
    handler.request.sendall(res.to_data())
