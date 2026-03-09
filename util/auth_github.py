from dotenv import load_dotenv
from util.response import Response
import os
load_dotenv()

def auth_github(request, handler):
    print(request.body)
    res = Response()

    res.set_status(302, "Found")
    #res.headers({"Location": 'https://github.com/login/oauth/authorize'})

    s = "https://github.com/login/oauth/authorize"
    #s = s + '?response_type=code'
    s = s + '?client_id=' + str(os.getenv("GITHUB_CLIENT_ID"))
    s = s + '&redirect_uri=http://localhost:8080/authcallback'

    res.headers({"Location": s})
    print(s)
    print("look here")


    handler.request.sendall(res.to_data())
