from util.response import Response


def host_path(request, handler):
    res = Response()
    path = request.path
    b = True

    print(path)
    print(path.__contains__(".gif"))
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
            with open("./" + path, "rb") as f:
                file_bytes = f.read()
            res.bytes(file_bytes)
        except FileNotFoundError:
            (
                print("file not found"))

        handler.request.sendall(res.to_data())
        return



    #INDEX.HTML
    #if path == "/" or path == "/chat":
    if path.startswith("/"):
        print("entered html with : " + path)
        if path == "/":
            path = "./public/index.html"
        elif path == "/chat":
            path = "./public/chat.html"
        else:
            path = "./public" + path + ".html"

        # if path == "/":
        #     path = "./public/index.html"
        # elif path == "/chat":
        #     path = "./public/chat.html"
        #elif path == "/settings":
            #path =

        with open("./public/layout/layout.html", "r", encoding="utf-8") as f:
            layout = f.read()
        with open(path, "r", encoding="utf-8") as f:
            contents = f.read()

        #print(layout)
        idx = layout.index("{{content}}")
        layout = layout[0:idx] + contents + layout[idx:0]

        #print("goooooooooooooooooooooooooooooal")
        res.text(layout)
        res.head["Content-Type"] = "text/html"
        handler.request.sendall(res.to_data())







