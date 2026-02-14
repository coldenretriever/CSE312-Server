from util.response import Response


def host_path(request, handler):
    res = Response()
    path = request.path


    #INDEX.HTML
    if path == "/" or path == "/chat":
        if path == "/":
            path = "./public/index.html"
        elif path == "/chat":
            path = "./public/chat.html"

        with open("./public/layout/layout.html", "r", encoding="utf-8") as f:
            layout = f.read()
        with open(path, "r", encoding="utf-8") as f:
            contents = f.read()

        print(layout)
        idx = layout.index("{{content}}")
        layout = layout[0:idx] + contents + layout[idx:0]

        #print("goooooooooooooooooooooooooooooal")
        res.text(layout)
        res.head["Content-Type"] = "text/html"
        handler.request.sendall(res.to_data())







    try:
        print(path)
        with open("./" + path, "rb") as f:
            file_bytes = f.read()
        res.bytes(file_bytes)
    except FileNotFoundError:(
        print("file not found"))

    if path.__contains__("html"):
        res.head["Content-Type"] = "text/html"
    elif path.__contains__(".js"):
        res.head["Content-Type"] = "text/javascript"
    elif path.__contains__(".jpg"):
        res.head["Content-Type"] = "image/jpeg"
    elif path.__contains__(".ico"):
        res.head["Content-Type"] = "image/x-icon"
    elif path.__contains__(".webp"):
        res.head["Content-Type"] = "image/webp"
    elif path.__contains__(".gif"):
        res.head["Content-Type"] = "image/gif"
    elif path.__contains__(".json"):
        res.head["Content-Type"] = "application/json"


    handler.request.sendall(res.to_data())