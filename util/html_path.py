from util.response import Response


def html_path(request, handler):
    res = Response()
    path = request.path
    b = True

    # INDEX.HTML
    # if path == "/" or path == "/chat":
    if path.startswith("/"):
        print("entered html with : " + path)
        if path == "/":
            path = "./public/index.html"
        elif path == "/chat":
            path = "./public/chat.html"
        else:
            path = "./public" + path + ".html"

        with open("./public/layout/layout.html", "r", encoding="utf-8") as f:
            layout = f.read()
        with open(path, "r", encoding="utf-8") as f:
            contents = f.read()

        # print(layout)
        idx = layout.index("{{content}}")
        layout = layout[0:idx] + contents + layout[idx:0]

        # print("goooooooooooooooooooooooooooooal")
        res.text(layout)
        res.head["Content-Type"] = "text/html"
        handler.request.sendall(res.to_data())







