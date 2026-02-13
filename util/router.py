from util.response import Response


class Router:

    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, action, exact_path=False):
        self.routes[(method, path)] = {"action": action, "exact_path": exact_path}
        #how do I want to store the paths so it can be compared?

    def route_request(self, request, handler):

        #Loop through all in dictionary I think
        #compare path to keys with startswith


        #HAVE TO ADD EXACT PATH CONDITION
        for key in self.routes.keys():
            if key[0] == request.method and (key[1] == request.path or (key[1].startswith(request.path))):# and self.routes[key]["exact_path"] == False)):
                print(request.path + "_________")
                print("key: " + key[0] + " path " + key[1])
                func = self.routes[key]["action"]
                func(request, handler)
                return

        res = Response()
        res.set_status(404, "Not Found")
        res.text("The requested content does not exist")
        handler.request.sendall(res.to_data())
