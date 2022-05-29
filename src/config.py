import os

from dotenv import load_dotenv

load_dotenv()

OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
OAUTH_REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI')

SERVER_PORT = int(os.getenv('SERVER_PORT', 8080))
