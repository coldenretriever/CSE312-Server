from util.response import Response


def index_path(request, handler):
    res = Response()

    #read and save the contents
    # -layout.html
    # -contents of request file
    #insert request file into
    # -contents of layout and
    # -put that into the response

    with open("public/layout/layout.html", "r", encoding="utf-8") as f:
        layout = f.read()
    with open(request.path, "r", encoding="utf-8") as f:
        contents = f.read()

    idx = layout.index("{{contents}}")
    layout = layout[0:idx] + contents + layout[idx:0]

    print("goooooooooooooooooooooooooooooal")
    res.text(layout)
    handler.request.sendall(res.to_data())
