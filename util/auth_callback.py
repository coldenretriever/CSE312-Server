import json

import requests
from dotenv import load_dotenv
from util.response import Response
import os
load_dotenv()

def auth_callback(request, handler):
    #print(request.path)

    print("Callback triggered:", request.path)
    pre, code = request.path.split("=", 1)
    #print(code)

    client_id = str(os.getenv("GITHUB_CLIENT_ID"))
    client_secret = str(os.getenv("GITHUB_CLIENT_SECRET"))

    url = "https://github.com/login/oauth/access_token"

    print("Sending code:", code)
    print("Client ID:", client_id)
    r = requests.post(url, headers={"Accept":"application/json"},data={'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': 'http://localhost:8080/authcallback'})
    print("Status:", r.status_code)
    print("Response:", r.text)
    v = json.loads(r.text)
    access_token = v["access_token"]

    a = requests.get("https://api.github.com/user", headers={"Authorization": "Bearer " + access_token})
    print("Status67:", a.status_code)
    print("Response:", a.text)

    res = Response()
    res.set_status(302, "passed everything go back")
    res.headers({"Location": "http://localhost:8080"})


    # print(r)
    # print(r.status_code)
    # print(r.text)

    handler.request.sendall(res.to_data())
