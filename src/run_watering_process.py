#!/usr/bin/env python3

from parse_config import get_configuration
from video_uploader import VideoUploader
from graph_handler import GraphHandler
from db_handler import DatabaseHandler
import requests
from logzero import logger


def main():
    """ Main entry point of the app """
    # Get configuration
    args = get_configuration()
    # Create Instagram Graph API handler object
    gh = GraphHandler(args)
    # Create video uploader object.
    video_uploader = VideoUploader(args)

    # Checking if the account needs to be configured.
    if args.configure_account:
        gh.create_configuration_files()
    else:
        dbh = DatabaseHandler(args)
        dbh.setup_table()
        dbh.cleanup()
    """else:
        # Upload video and get url to it.
        video_url = video_uploader.upload_video()
        if video_url:
            logger.info("Video url is: " + video_url)
            gh.start_posting_process(video_url)"""


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
