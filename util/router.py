from util.chat_path import chat_path
from util.host_path import host_path
from util.response import Response


class Router:

    def __init__(self):
        self.methods = []
        self.paths = []
        self.actions = []
        self.exact_paths = []
        self.index = 0

    def add_route(self, method, path, action, exact_path=False):
        self.methods.append(method)
        self.paths.append(path)
        self.actions.append(action)
        self.exact_paths.append(exact_path)
        self.index = self.index + 1

    def route_request(self, request, handler):
        for i in range(self.index):
            method = self.methods[i]
            path = self.paths[i]
            exact_path = self.exact_paths[i]
            if method == request.method and (path == request.path or (request.path.startswith(path) and exact_path == False)):
                print("sent " + request.path + " to " + method + " " + path)
                func = self.actions[i]
                func(request, handler)
                return

        res = Response()
        res.set_status(404, "Not Found")
        res.text("The requested content does not exist")
        handler.request.sendall(res.to_data())