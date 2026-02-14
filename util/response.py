import json


class Response:

    def __init__(self):
        #do I just want to maintain
        #data structures and then add in to_data?
        self.http_version = "HTTP/1.1"
        self.status_code = 200
        self.status_message = "OK"
        self.head = {}
        self.body = b""
        self.cookList = []

        self.head["Content-Type"] = "text/plain; charset=utf-8"
        self.head["X-Content-Type-Options"] = "nosniff"


    def set_status(self, code, text):
        self.status_code = code
        self.status_message = text
        return self

    def headers(self, headers):
        for key in list(headers.keys()):
            self.head[key] = headers[key]
        return self


    def cookies(self, cookies):
        for key in list(cookies.keys()):
            entry = ""
            entry = entry + key + "=" + cookies[key]
            self.cookList.append(entry)
        return self

    def bytes(self, data):
        self.body = self.body + data
        return self

    def text(self, data):
        if isinstance(data, str):
            self.bytes(data.encode("utf-8"))
        return self

    def json(self, data):
        json_string = json.dumps(data)
        bytes_json = json_string.encode("utf-8")
        self.body = bytes_json
        self.head["Content-Type"] = "application/json"

        return self

    def to_data(self):
        data = b""

        #status line
        data = data.__add__(self.http_version.encode("utf-8"))
        data = data.__add__(b" " + str(self.status_code).encode("utf-8"))
        data = data.__add__(b" " + self.status_message.encode("utf-8") + b"\r\n")

        #headers
        self.head["Content-Length"] = str(len(self.body))
        for key in self.head.keys():
            data = data.__add__(key.encode("utf-8") + b": " + self.head[key].encode("utf-8") + b"\r\n")

        #cookies
        for i in range(len(self.cookList)):
            data = data.__add__(b"Set-Cookie: " + self.cookList[i].encode("utf-8") + b"\r\n")

        data = data.__add__(b"\r\n")

        #body
        data = data.__add__(self.body)

        return data







def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    if actual != expected:
        print("failed")
        print(actual)

def test2():
    res = Response()
    res.text("test 123")
    res.set_status(67, "41")
    res.headers({"a":"b", "c":"d"})
    res.headers({"e":"f", "g":"h"})

    res.cookies({"a":"b", "c":"d"})
    #res.json(["1", "2", "3"])
    res.cookies({"a":"c"})
    res.bytes(b"should be last")
    expected = b'HTTP/1.1 67 "41"\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    #test_json = res.json("hello y'all")
    if actual != expected:
        print("failed")
        print(actual)

def test_overwrite():
    res = Response()
    res.headers({"Content-Type": "this guy"})
    res.json(["1", "2", "3"])
    actual = res.to_data()
    print(actual)
    assert actual.__contains__(b'Content-Length: 15')
    assert actual.__contains__(b'X-Content-Type-Options: nosniff')
    assert actual.__contains__(b'200')

    res.json({"1":"a"})
    assert res.body == b'{"1": "a"}'
    actual = res.to_data()
    assert not actual.__contains__(b'3')
    print(actual)

def test_cookies():
    res = Response()
    res.cookies({"Is":"there", "a":"space"})
    res.bytes(b"\r\n\r\nThere all all of these characters")
    actual = res.to_data()
    print(actual)
    assert actual.__contains__(b"space")
    assert actual.__contains__(b"\r\n\r\nThere all all of these characters")

def test_final():
    res = Response()
    res.set_status(566, "this is an important one")
    res.headers({"One":"Aight"})
    res.headers({"One": "Two", "Banana": "Sprinkled Donut"})
    res.bytes(b"supercalifragilistic")
    res.text("hello y'all")
    res.cookies({"cookie1":"des1", "2222cookies":"GOODCOOKIE"})
    res.cookies({"cookie3":"des2", "2222c3okies":"GOO4COOKIE"})

    actual = res.to_data()
    print(actual)
    assert actual.__contains__(b"566 this is an important one\r\n")
    assert actual.__contains__(b"HTTP/1.1")
    assert actual.__contains__(b"One: Two\r\n")
    assert actual.__contains__(b"Banana: Sprinkled Donut\r\n")
    assert actual.__contains__(b"supercalifragilistic")
    assert actual.__contains__(b"hello y'all")
    assert actual.__contains__(b"Set-Cookie: cookie1=des1\r\nSet-Cookie: 2222cookies=GOODCOOKIE\r\nSet-Cookie: cookie3=des2\r\nSet-Cookie: 2222c3okies=GOO4COOKIE\r\n")

    res.json({"Will it overwrite?":"I don't know"})
    actual = res.to_data()
    print(actual)
    assert actual.__contains__(b"Will it overwrite?")
    assert actual.__contains__(b"application/json")
    assert not actual.__contains__(b"text/plain")
    assert not actual.__contains__(b"hello y'all")

def test_cookies2():
    res = Response()
    res.cookies({"One": "two", "3":"4"})
    res.cookies({"five": "six", "seven":"8"})
    actual = res.to_data()
    print(actual)
    assert actual.__contains__(b"\r\nSet-Cookie: One=two\r\nSet-Cookie: 3=4\r\nSet-Cookie: five=six\r\nSet-Cookie: seven=8\r\n")


if __name__ == '__main__':
    test1()
    test2()
    test_overwrite()
    test_cookies()
    test_final()
    test_cookies2()

