from idlelib.rpc import request_queue


class Router:

    def __init__(self):
        self.routes = {}
        self.funcs = {}


    def add_route(self, method, path, action, exact_path=False):
        self.routes[(method, path)] = action


    def route_request(self, request, handler):
        if self.routes.keys().__contains__((request.http_version, request.path)):
            self.routes[(request.http_version, request.path)](request, handler)
        else:
            handler.request.sendall("404 Not Found")
