from util.response import Response


def host_path(request, handler):
    res = Response()
    path = request.path
    print("\n\n" + path + "\n")
    with open(path, "rb") as f:
        file_bytes = f.read()
    res.bytes(file_bytes)

    if path.__contains__("html"):
        res.headers["Content-Type"] = "text/html"
    elif path.__contains__(".js"):
        res.headers["Content-Type"] = "text/javascript"
    elif path.__contains__(".jpg"):
        res.headers["Content-Type"] = "image/jpeg"
    elif path.__contains__(".ico"):
        res.headers["Content-Type"] = "image/x-icon"
    elif path.__contains(".webp"):
        res.headers["Content-Type"] = "image/webp"





    handler.request.sendall(res.to_data())
