import argparse
import os.path

from authorization import authorization
from config import SERVER_PORT
from filesystem import filesystem
from google import google
from logger import logger
from server import server, Request, Response


parser = argparse.ArgumentParser()
parser.add_argument("src", help="directory with images")


@server.get('/auth/google/callback')
def auth_callback(req: Request, res: Response):
    code = req.query.get('code')
    token = authorization.get_token(code=code)
    google.access_token = token['access_token']

    logger.log('Authenticated successfully')

    res.send('Authenticated successfully. Go back to the terminal.')
    server.stop()


if __name__ == '__main__':
    args = parser.parse_args()
    configuration = vars(args)
    absolute_path = os.path.abspath(configuration.get('src', '.'))

    logger.log('Getting auth URL...')

    auth_url = authorization.get_auth_url()

    logger.log(f"Click the link below to login using your Google account\n{auth_url}")

    server.run(port=SERVER_PORT)

    filesystem.observe(absolute_path)
