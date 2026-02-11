import json


class Response:

    def __init__(self):
        #do I just want to maintain
        #data structures and then add in to_data?
        self.http_version = "HTTP/1.1"
        self.status_code = 200
        self.status_message = "OK"
        self.head = {}
        self.body : bytes = b""

        self.head["Content-Type"] = "hasn't been set"


    def set_status(self, code, text):
        self.status_code = code
        self.status_message = text
        return self

    def headers(self, headers):
        for key in list(headers.keys):
            self.head[key] = headers[key]
        return self


    def cookies(self, cookies):
        self.head["Set-Cookie"] = ""
        for key in list(cookies.keys):
            self.head["Set-Cookie"] = (self.head["Set-Cookie"]
                                       + key + "=" + cookies[key] + ";")

        self.head["Set-Cookie"] = self.head["Set-Cookie"][:len(self.head["Set-Cookie"]) - 1]
        return self

    def bytes(self, data):
        self.body = self.body + data
        return self

    def text(self, data):
        data = data.encode("utf-8")
        self.body = self.body + data
        return self

    def json(self, data):
        #I have to interpret the string/dict
        #format it into json format
        #then encode in utf-8 to bytes
        #set to body
        #change Content-Type header to application/json

        json_string = json.dumps(data)
        bytes_json = json_string.encode("utf-8")
        self.body = bytes_json
        self.head["Content-Type"] = "application/json"



        return self

    def to_data(self):
        #SET NO-SNIFF HEADER
        #
        #
        #
        #
        #
        self.http_version = self.http_version.encode("utf-8")
        self.status_code = str(self.status_code).encode("utf-8")
        self.status_message = self.status_message.encode("utf-8")

        dat = b""
        dat = self.http_version + b" " + self.status_code + b" " + self.status_message + b"\r\n"

        if self.head["Content-Type"] == "hasn't been set":
            self.head["Content-Type"] = " text/plain; charset=utf-8"

        for key in list(self.head.keys()):
            dat = dat + key.encode("utf-8") + b":" + self.head[key].encode("utf-8") + b"\r\n"
        #need to add
        #   Content-Length
        #   No-Sniff
        dat = dat + b"X-Content-Type-Options: nosniff" + b"\r\n"
        dat = dat + b"Content-Length: " + str(len(self.body)).encode("utf-8") + b"\r\n"
        dat = dat + b"\r\n"
        dat = dat + self.body

        return dat


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    if actual != expected:
        print("failed")
        print(actual)


if __name__ == '__main__':
    test1()

