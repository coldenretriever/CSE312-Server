from util.response import Response


def chat_path(request, handler):
    res = Response()


    handler.request.sendall(res.to_data())
