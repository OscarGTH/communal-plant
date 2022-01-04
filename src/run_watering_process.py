#!/usr/bin/env python3

from parse_config import get_configuration
from video_uploader import VideoUploader
from graph_handler import GraphHandler
import requests
from logzero import logger



def main():
    """ Main entry point of the app """
    # Get configuration
    args = get_configuration()
    # Create Instagram Graph API handler object
    gh = GraphHandler(args)

    # Checking if the account needs to be configured.
    if args.configure_account:
        gh.create_configuration_files()
    else:
        logger.info("TBD")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()