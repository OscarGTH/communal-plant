#!/usr/bin/env python3

from datetime import datetime
from parse_config import get_configuration
from graph_handler import GraphHandler
from db_handler import DatabaseHandler
from logzero import logger


def get_media_id(dbh):
    """ Fetches media id for current day's post from database and returns it."""

    # Get current date
    date = datetime.now().date()
    media_id = dbh.get_post_by_date(date)
    return media_id


def main():
    """ Main entry point of the app """
    # Get configuration
    args = get_configuration()
    # Create Instagram Graph API handler object
    gh = GraphHandler(args)
    dbh = DatabaseHandler(args)
    media_id = get_media_id(dbh)
    if media_id:
        logger.info("Media id received, getting comments for the post.")
        comments = gh.get_comments_for_post(media_id)
        logger.info(comments)
    else:
        logger.info(
            "Comments cannot be checked so using default value as water amount.")
        # TODO: Insert values to database.
    dbh.cleanup()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
