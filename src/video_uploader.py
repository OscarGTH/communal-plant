#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
from logzero import logger

class VideoUploader:

    def __init__(self, args) -> None:
        self.args = args

    def upload_video(self):
        """ Reads video file and posts it. """

        logger.info("Starting video upload process.")
        # Get UTC timestamp 10 minutes ahead of program running time.
        expiry_date = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        url = self.args.file_io_base_path
        # Set headers and payload
        header = {"accept": "application/json",
                  "Authorization": 'Bearer ' + self.args.file_io_api_key}
        payload = {'expires': expiry_date,
                   'maxDownloads': 1,
                   'autoDelete': True}

        logger.info("Opening video file.")
        # Creating empty object to store the video in.
        video = bytes()
        # Read video file
        try:
            with open('static/test.mp4', 'rb') as file:
                logger.info("Reading video into a bytes object.")
                # Read video bytes into variable.
                video = file.read()
        # File wasn't found
        except FileNotFoundError as fnfe:
            logger.error(fnfe)
        # Reading error
        except OSError as oe:
            logger.error(oe)
        # Other errors
        except Exception as err:
            logger.exception(err)

        # If video was read, continue.
        if video:
            # Send request.
            resp = requests.post(url, headers=header, params=payload, files={'file': video})
            print(resp.json())
