#!/usr/bin/env python3


import sqlite3
from logzero import logger


class DatabaseHandler:

    def __init__(self, args) -> None:
        with sqlite3.connect(args.database_name) as con:
            self.con = con
            self.cur = self.con.cursor()

    def cleanup(self):
        """ Closes connection to database. """

        self.con.close()

    def setup_table(self):
        """ Creates new table if it doesn't exist. """

        self.cur.execute(''' CREATE TABLE IF NOT EXISTS posts
                             (id integer, date text, water_amount integer, vote_count integer) ''')
        # Commiting changes.
        self.con.commit()

    def check_if_exists(self):
        """ Checks if posts table exists. """

        self.cur.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='posts'")
        # Check if the table exists.
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            logger.info("Table does not exist in the database.")
            return False

    def insert_to_table(self, payload):
        """ Inserts payload into posts database before post is published. """

        # Check that table exists.
        if self.check_if_exists:
            required_keys = set(['date', 'water_amount', 'vote_count'])
            # Make sure that required values are present.
            if required_keys.issubset(payload.keys()):
                # Create SQL expression
                sql = (
                    "INSERT INTO posts (date, water_amount, vote_count) VALUES (?, ?, ?)")
                # Execute insertion to database.
                self.cur.execute(
                    sql, (payload['date'], payload['water_amount'], payload['vote_count']))
                # Commit changes.
                self.con.commit()
            else:
                logger.error(
                    "Missing keys from payload when inserting into database.")

    def update_media_id(self, media_id, date):
        """ Updates IG Media id to post entry after it is published. """

        # Update media id where date matches.
        sql = ("UPDATE posts SET id = ? WHERE date = ?")
        self.cur.execute(sql, (media_id, date))
        # Commit changes.
        self.con.commit()

    def get_all(self):
        """ Prints the whole posts table. """

        sql = ("SELECT * FROM posts")
        # Print every row
        for row in self.cur.execute(sql):
            logger.info(row)

    def is_first_post(self):
        """ Returns boolean value telling if there are post entries in the table."""

        if self.check_if_exists():
            # Select count of dates from the posts table.
            sql = ("SELECT count(date) FROM posts")
            self.cur.execute(sql)
            # If count is zero, table has no entries.
            if self.cur.fetchone()[0] == 0:
                logger.info("Table has entries.")
                return True
            else:
                return False
        else:
            return True

    def get_post_by_date(self, date):
        """ Returns the media id of post by date. """

        sql = ("SELECT id FROM posts WHERE date = ?")
        # Execute query.
        self.cur.execute(sql, (date,))
        try:
            # Get first result.
            media_id = self.cur.fetchone()[0]
            # Return result.
            return media_id
        except TypeError as ex:
            logger.error("Post not found by given date.")
            return None
