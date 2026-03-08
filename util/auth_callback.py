from util.response import Response
import request

def auth_callback(request, handler):
    res = Response()
    print(request.path)

    pre, code = request.path.split("=", 1)

    s = "https://github.com/login/oauth/access_token"
    #s.__add__('?response_type=code')
    s.__add__('&client_id=Ov23liVGBkf95tkcUCpu')
    s.__add('&client_secret=8c94cd25a837d2762939869130ce306135031a3c')
    s.__add__('&' + code)
    s.__add__('&redirect_uri=http://localhost:8080/authcallback')

    response = request.post(s)