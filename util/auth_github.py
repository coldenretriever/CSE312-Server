from util.response import Response


def auth_github(request, handler):
    print(request.body)
    res = Response()

    res.set_status(302, "Found")
    #res.headers({"Location": 'https://github.com/login/oauth/authorize'})

    s = "https://github.com/login/oauth/authorize"
    s.__add__('?response_type=code')
    s.__add__('&client_id=Ov23liVGBkf95tkcUCpu')
    #s.__add__('&scopes='
    s.__add__('&redirect_uri=http://localhost:8080/authcallback')

    res.headers({"Location": s})


    handler.request.sendall(res.to_data())
