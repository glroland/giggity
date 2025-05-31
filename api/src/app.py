import os
import requests
from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

oauth = OAuth(app)
oauth.register(
    name='github',
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    access_token_url=os.environ["TOKEN_URL"],
    access_token_params=None,
    authorize_url=os.environ["AUTHORIZE_URL"],
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route("/api/public")
def public():
    response = (
        "Hello from a public endpoint! You don't need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)

@app.route("/api/private")
def private():
    token = oauth.github.authorize_access_token()
    print(token['userinfo'])

    response = (
    "Hello from a private endpoint! You need to be"
    " authenticated to see this."
    )
    return jsonify(message=response)
