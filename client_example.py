from flask import Flask, redirect, url_for, request, jsonify, session
import requests

app = Flask(__name__)

app.secret_key = 'your_secret_key'
# OAuth server endpoints
AUTHORIZATION_ENDPOINT = 'http://127.0.0.1:5000/signin'
TOKEN_ENDPOINT = 'http://127.0.0.1:5000/api/get_token'
USERINFO = 'http://127.0.0.1:5000/api/get_user'

# Client credentials
CLIENT_ID = '379b045bf18e4b1588cb8188de166538'
CLIENT_SECRET = 'xXTZD9hmk7M1KUoD93X0hQ'


# Client homepage
@app.route('/')
def home():
    if session.get('email'):
        return f'<h1>Welcome {session.get("email")}</h1> <br> <a href="/logout">Logout</a>'
    return '<h1>Welcome to OAuth Client</h1><a href="/login">Login</a>'

# Authorization callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed'

    # Exchange authorization code for access token
    data = {
            "code":code
            }
    code_headers = {'Content-Type': 'application/json'}
    response = requests.post(TOKEN_ENDPOINT, json=data, headers=code_headers)
    if response.status_code != 200:
        return response.json()
    access_token = response.json().get('access_token')
    token_data = {
            "access_token":access_token,
            "app_id":CLIENT_ID,
            "api_key":CLIENT_SECRET
    }
    user_data = requests.post(USERINFO, json=token_data, headers=code_headers)
    session['access_token'] = access_token
    session['email'] = user_data.json()['email']
    session['id'] = user_data.json()['_id']
    return redirect(url_for('home'))

# Initiate authorization flow
@app.route('/login')
def login():
    return redirect(AUTHORIZATION_ENDPOINT + f"/{CLIENT_ID}")

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
