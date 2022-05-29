from requests_oauth2.services import GoogleClient

from config import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI


class Authorization:
    def __init__(self):
        self.google_auth = GoogleClient(
            client_id=OAUTH_CLIENT_ID,
            client_secret=OAUTH_CLIENT_SECRET,
            redirect_uri=OAUTH_REDIRECT_URI
        )

    def get_auth_url(self):
        scope = [
            "https://www.googleapis.com/auth/photoslibrary.readonly",
            "https://www.googleapis.com/auth/photoslibrary.appendonly"
        ]
        return self.google_auth.authorize_url(scope=scope, response_type='code')

    def get_token(self, code: str):
        return self.google_auth.get_token(code=code, grant_type='authorization_code')


authorization = Authorization()
