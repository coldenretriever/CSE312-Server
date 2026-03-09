import json
import base64

import requests
from dotenv import load_dotenv

from util.github_session import github_session
from util.response import Response
import os
load_dotenv()

def auth_callback(request, handler):

    pre, code = request.path.split("=", 1)

    client_id = str(os.getenv("GITHUB_CLIENT_ID"))
    client_secret = str(os.getenv("GITHUB_CLIENT_SECRET"))

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_encoded = base64.b64encode(auth_bytes, altchars=None)
    auth_toSend = auth_encoded.decode("utf-8")

    url = "https://github.com/login/oauth/access_token"

    print("Sending code:", code)
    print("Client ID:", client_id)
    r = requests.post(url, headers={"Accept":"application/json", "Authorization": "Basic " + auth_toSend},data={'code': code, 'redirect_uri': 'http://localhost:8080/authcallback'})
    print("Status:", r.status_code)
    print("Response:", r.text)
    v = json.loads(r.text)
    access_token = v["access_token"]

    a = requests.get("https://api.github.com/user", headers={"Authorization": "Bearer " + access_token})
    print("Status67:", a.status_code)
    print("Response:", a.text)

    output = json.loads(a.text)
    github_session(output["login"], handler)