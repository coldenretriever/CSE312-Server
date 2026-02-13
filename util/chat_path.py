from util.response import Response


def chat_path(request, handler):
    res = Response()
    path = request.path
    try:
        print(path)
        with open(path, "rb") as f:
            file_bytes = f.read()
        res.bytes(file_bytes)
    except FileNotFoundError:
        (
            print("file not found"))

    handler.request.sendall(res.to_data())
