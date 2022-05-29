import os
import time

import watchdog.events
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from google import google
from logger import logger


class NewFileEvent(PatternMatchingEventHandler):
    patterns = ['*.jpg', '*.jpeg']

    @staticmethod
    def process(event):
        if event.event_type == watchdog.events.EVENT_TYPE_CREATED:
            filesystem.files_to_upload.append(event.src_path)

    def on_created(self, event):
        self.process(event)


class Filesystem:
    def __init__(self):
        self.uploaded_files = []
        self.files_to_upload = []

    def observe(self, path: str):
        logger.log(f"Observing directory {path}", scope="Filesystem")

        observer = Observer()
        observer.schedule(NewFileEvent(), path, recursive=True)
        observer.start()

        logger.log("Filesystem observer started", scope="Filesystem")

        counter = 0

        try:
            while True:
                if counter >= 30:
                    self.get_uploaded_files()
                    self.upload_files()
                    counter = 0
                else:
                    counter += 1
                    time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logger.log('Filesystem observer stopped', scope="Filesystem")

    def get_uploaded_files(self):
        logger.log("Get already uploaded files", scope="Observer")
        self.uploaded_files = google.get_filenames()

    def upload_files(self):
        if len(self.files_to_upload) == 0:
            logger.log("No files to upload", scope="Observer")
            return

        filepaths = []

        while len(self.files_to_upload) > 0:
            filepath = self.files_to_upload.pop()
            filename = os.path.basename(filepath)

            if filename not in self.uploaded_files:
                filepaths.append(filepath)
            else:
                logger.log(f"File {filename} has been already uploaded. Skipping", scope="Observer")

        google.upload_files(filepaths)


filesystem = Filesystem()
