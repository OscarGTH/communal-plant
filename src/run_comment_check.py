#!/usr/bin/env python3

from datetime import datetime, timedelta
import re
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


def sanitize_comment(comment):
    """ Removes unwanted characters from a string that could be harmful. """

    unwanted = "\"();:\'"
    # Replacing unwanted characters with None
    sanitized = comment.translate({ord(i): None for i in unwanted})
    return sanitized


def parse_comments(comments):
    """ Parses comments and checks which water amount wins the vote."""

    vote_result = {'water_amount': 0, 'vote_count': 0}
    votes = dict()
    # Iterating through every comment
    for comment in comments:
        sanitized = sanitize_comment(comment['text'])
        logger.info("Comment: " + sanitized)
        match = re.search("[0-9][0-9]?\s?(ml)", sanitized)
        if match:
            # Get match
            result = match.group(0)
            # Remove whitespace and milliliter characters.
            amount = str(result.translate({ord(i): None for i in " ml"}))
            if amount in votes:
                votes[amount] += 1
            else:
                votes[amount] = 1
    if votes:
        water_amount = max(votes, key=votes.get)
        vote_result['water_amount'] = int(water_amount)
        vote_result['vote_count'] = int(votes[water_amount])
        logger.info("Voted amount of water is: " + water_amount + " ml.")
    else:
        logger.warning("No votes found.")
    return vote_result


def set_vote_results_to_db(dbh, result):
    """ Takes vote results to database. """

    # Get tomorrows date and set it to dictionary.
    result['date'] = datetime.now().date() + timedelta(days=1)
    logger.info("Inserting vote results into table.")
    dbh.insert_to_table(result)
    dbh.get_all()


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
        logger.info("Parsing comments.")
        # Get most voted water amount and vote count.
        result = parse_comments(comments)
        # Set result to database for tomorrow's entry.
        set_vote_results_to_db(dbh, result)
    else:
        logger.info(
            "Comments cannot be checked so using default value as water amount.")
        # Update database with zeroes.
        set_vote_results_to_db(dbh, {'water_amount': 0, 'vote_count': 0})

    dbh.cleanup()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
