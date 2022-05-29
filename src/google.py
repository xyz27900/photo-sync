import json
import os

import requests
from requests import Session
from requests_oauth2 import OAuth2BearerToken

from logger import logger


class Google:
    def __init__(self):
        self.access_token = None

    def get_filenames(self):
        if not self.access_token:
            logger.log('Access token was not specified', scope="Google")
            return

        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            res = session.get('https://photoslibrary.googleapis.com/v1/mediaItems')
            res.raise_for_status()
            data = res.json()

        filenames = map(lambda item: item['filename'], data['mediaItems'])

        return list(filenames)

    def upload_files(self, filepaths: list):
        if not self.access_token:
            logger.log('Access token was not specified', scope="Google")
            return

        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            session.headers["Content-type"] = "application/octet-stream"
            session.headers["X-Goog-Upload-Protocol"] = "raw"

            for filepath in filepaths:
                self.upload_file(session, filepath)

    @staticmethod
    def upload_file(session: Session, filepath: str):
        filename = os.path.basename(filepath)
        session.headers["X-Goog-Upload-File-Name"] = filename
        file = open(filepath, mode='rb')
        file_content = file.read()

        logger.log(f"Uploading file {filename}", scope="Google")
        res = session.post('https://photoslibrary.googleapis.com/v1/uploads', data=file_content)

        if res.status_code == 200 and res.content:
            media_item = {
                'albumId': None,
                'newMediaItems': [{
                    'description': '',
                    'simpleMediaItem': {
                        'uploadToken': res.content.decode()
                    }
                }]
            }

            json_data = json.dumps(media_item, indent=4)
            Google.finish_upload(session, json_data, filename)
        else:
            logger.log(f"Could not upload {filename}: {res.json()}", scope="Google")

    @staticmethod
    def finish_upload(session: Session, data: str, filename: str):
        res = session.post('https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', data=data).json()

        if 'newMediaItemResults' in res:
            status = res['newMediaItemResults'][0]['status']

            if status.get('code', 0) > 0:
                logger.log(f"Could not upload {filename}: {status['message']}", scope="Google")
            else:
                logger.log(f"File {filename} uploaded successfully", scope="Google")
        else:
            logger.log(f"Could not upload {filename}: {res}", scope="Google")


google = Google()
