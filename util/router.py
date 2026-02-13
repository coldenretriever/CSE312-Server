class Router:

    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, action, exact_path=False):
        self.routes[(method, path)] = {"action": action, "exact_path": exact_path}
        #how do I want to store the paths so it can be compared?

    def route_request(self, request, handler):

        #Loop through all in dictionary I think
        #compare path to keys with startswith

        fail = True
        for key in self.routes.keys():
            if key[0] == request.method and (key[1] == request.path or key[1].startswith(request.path)):
                self.routes[key](request, handler)
                fail = False

        if fail:
            handler.request.sendall("404 Not Found")
