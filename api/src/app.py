import json
import requests
from flask import Flask, jsonify, request
from authlib.integrations.flask_oauth2 import ResourceProtector
from token_validator import MyBearerTokenValidator
from constants import GITHUB_API_BASE_URL, SCOPE_READ_REPO

# display config
print ("Giggity API Server...")
print ()

# flask app
app = Flask(__name__)

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
@require_oauth(SCOPE_READ_REPO)
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
