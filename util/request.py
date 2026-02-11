


class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}

        prev, self.body = request.split(b"\r\n\r\n", 1)
        prev = prev.decode("utf-8")

        #short term, need to parse all headers regardless
        lines = prev.split("\r\n")
        i = 0
        for line in lines:
            i = i + 1
            if i == 1:
                self.method, self.path, self.http_version = line.split(" ", 2)
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "Cookie":
                cookies = line.split(";")
                for cookie in cookies:
                    name, cook = cookie.split("=")
                    name = name.split()
                    cook = cook.split()
                    self.cookies[name] = cook

            self.headers[key] = value



def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

    print("passed all tests")


if __name__ == '__main__':
    test1()

