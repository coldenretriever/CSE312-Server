from util.response import Response


def host_path(request, handler):
    res = Response()
    path = request.path
    b = True

    if path.__contains__(".js"):
        res.head["Content-Type"] = "text/javascript"
    elif path.__contains__(".jpg"):
        res.head["Content-Type"] = "image/jpeg"
    elif path.__contains__(".ico"):
        res.head["Content-Type"] = "image/x-icon"
    elif path.__contains__(".webp"):
        res.head["Content-Type"] = "image/webp"
    elif path.__contains__(".gif"):
        print("got in with: " + path)
        res.head["Content-Type"] = "image/gif"
    elif path.__contains__(".json"):
        res.head["Content-Type"] = "application/json"
    else:
        b = False

    if b:
        print("IIIIII")
        try:
            print(path)
            if path.__contains__(".js"):
                with open("./" + path, "r", encoding="utf-8") as f:
                    file_bytes = f.read()
                res.text(file_bytes)
            else:
                with open("./" + path, "rb") as f:
                    file_bytes = f.read()
                res.bytes(file_bytes)
        except FileNotFoundError:
            (
                print("file not found"))

        handler.request.sendall(res.to_data())
        return





