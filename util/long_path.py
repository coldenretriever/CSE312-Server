from util.response import Response


# This path is provided as an example of how to use the router
def long_path(request, handler):
    print("Got there!")
    res = Response()
    res.text("Hey there!")
    res.json({"1": 1})
    handler.request.sendall(res.to_data())
