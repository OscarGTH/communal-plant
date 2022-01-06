#!/usr/bin/env python3

from parse_config import get_configuration
from video_uploader import VideoUploader
from graph_handler import GraphHandler
from db_handler import DatabaseHandler
from logzero import logger


def main():
    """ Main entry point of the app """
    # Get configuration
    args = get_configuration()
    # Create Instagram Graph API handler object
    gh = GraphHandler(args)
    # Create video uploader object.
    video_uploader = VideoUploader(args)
    dbh = DatabaseHandler(args)
    # Check if it is not first post.
    if not dbh.check_if_first_post():
        logger.info("Doing normal run")
        # Upload video and get url to it.
        """video_url = video_uploader.upload_video()
        if video_url:
            logger.info("Video url is: " + video_url)
            media_dict = gh.start_posting_process(video_url)
            logger.info(media_dict)
        """
    else:
        logger.info("Doing first run.")
    dbh.cleanup()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
