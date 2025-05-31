import os
import json
import requests
from flask import Flask, jsonify, request
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator

# constants
GITHUB_API_BASE_URL = "https://api.github.com/"
SCOPE = "user:email"

# environment variables
ENV_FLASK_SECRET_KEY = "FLASK_SECRET_KEY"

# config
flask_secret_key = os.environ[ENV_FLASK_SECRET_KEY]

# display config
print ("Giggity API Server...")
print ()
print ("Flask Secret Key = '" + flask_secret_key + "'")
print ()

# flask app
app = Flask(__name__)
app.secret_key = flask_secret_key

# Define a validator for bearer tokens
class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        url = GITHUB_API_BASE_URL + 'user'
        print ("Token: ", token_string)
        headers = {'Authorization': f'Bearer {token_string}'}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        # You can extract user info or scopes from resp.json() as needed
        # For example, get the scopes
        scopes = resp.headers.get('X-OAuth-Scopes', '').split(', ')
        print ("Scopes: ", scopes)
        return {'active': True, 'scope': scopes} # Return introspection response, active should be True if valid

    def validate_token(self, token, scopes, request):
        print ("Validating token...")
        if not token:
            print("Invalid Token - None")
            return False
        if not token['active']:
            print ("Token not active")
            return False

        #print (request.headers)
        #introspect_response = self.authenticate_token(request.headers["Authorization"])

        if scopes:
            print ("scopes")
            # Check if all the required scopes are granted
            granted_scopes = token.get('scope', [])
            if not all(s in granted_scopes for s in scopes):
                print ("missing scopes")
                return False

        print ("all scopes")
        return True

# Create a resource protector
require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())

@app.route("/")
def public():
    response = (
        "Hello from a public endpoint!"
    )
    return jsonify(message=response)

@app.route("/private")
@require_oauth()
def private():
    response = (
        "Hello from a private endpoint! You need to be authenticated to see this."
    )
    return jsonify(message=response)

@app.route("/contents/<repo_owner>/<repo_name>", methods=["GET", "POST"])
@require_oauth("repo")
def contents(repo_owner, repo_name):
    oauth_token = request.headers.get('Authorization').replace("Bearer ", "")
    print ("OAuth Token:", oauth_token)

    url = GITHUB_API_BASE_URL + "repos/" + repo_owner + "/" + repo_name + "/contents/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {oauth_token}",
    }
    data = {}

    response = requests.get(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    contents_response = json.loads(response.text)
    contents = []
    for file_obj in contents_response:
        contents.append(file_obj["name"])

    return jsonify(message=contents)


if __name__ == "__main__":
    app.run(debug=True)
