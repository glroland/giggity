import requests
from authlib.oauth2.rfc6750 import BearerTokenValidator
from constants import GITHUB_API_BASE_URL

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

        if scopes:
            print ("Scopes specified.  Checking each")

            # Check if all the required scopes are granted
            granted_scopes = token.get('scope', [])
            if not all(s in granted_scopes for s in scopes):
                print ("Scopes were missing from grants")
                return False

        print ("Token Validated!")
        return True
