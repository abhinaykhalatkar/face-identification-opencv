
import requests,time,os,webbrowser,threading
from flask import Flask, request, redirect
from threading import Thread
from credentials import client_id,client_secret,tenant_id

app_running = True 
def stop_flask_app():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    else:
        os._exit(0) 
    
token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
redirect_uri = 'http://localhost:8085/callback'

auth_url = (f'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
           f'?client_id={client_id}'
           f'&response_type=code'
           f'&redirect_uri={redirect_uri}'
           f'&response_mode=query'
           f'&scope=https://graph.microsoft.com/.default')


app = Flask(__name__)
access_token = ""

@app.route('/login')
def login():
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'response_mode': 'query',
        'scope': 'https://graph.microsoft.com/.default',
        'state': '12345'
    }
    auth_req_url = requests.Request('GET', auth_url, params=params).prepare().url
    return redirect(auth_req_url)

@app.route('/callback')
def callback():
    global app_running
    global access_token
    code = request.args.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(token_url, data=token_data)
    token_response_data = response.json()
    access_token = token_response_data.get('access_token')
    expires_in = token_response_data.get('expires_in', 3600)
    expiry_time = time.time() + expires_in
 
    if access_token: 
        with open("src/cred/token.txt", "w") as f:
            f.write(access_token)
        with open('src/cred/token_expiry_time.txt', 'w') as f:
            print(expiry_time)
            f.write(str(expiry_time))
        app_running = False
        stop_flask_app()
        return "Logged in successfully! You can close this window."
    else:
        error_description = token_response_data.get('error_description', 'Unknown error')
        return f"Failed to retrieve access token. Error: {error_description}"
    


def start_authentication():
    print(auth_url)
    webbrowser.open(auth_url, new=2)

if __name__ == "__main__":
    threading.Thread(target=start_authentication).start()

    t = Thread(target=app.run, kwargs={'debug': False, 'port': 8085, 'use_reloader': False})
    t.start()
    while app_running: 
        time.sleep(1) 

    t.join() 


