import socketserver

from util.chat_path import chat_path
from util.host_path import host_path
from util.index_path import index_path
from util.long_path import long_path
from util.request import Request
from util.router import Router
from util.hello_path import hello_path


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        #self.router.add_route("GET", "/hello", hello_path, True)
        # TODO: Add your routes here
        #self.router.add_route("GET", "/hello", long_path, False)
        self.router.add_route("POST", "/api/chats", chat_path, False)

        self.router.add_route("GET", "/api/chats", chat_path, False)
        self.router.add_route("GET", "/public", host_path, False)

        self.router.add_route("GET", "/", host_path, False)
        self.router.add_route("GET", "/chat", chat_path, False)


        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
