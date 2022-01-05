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
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS posts
                             (id integer, date text, water_amount integer, vote_count integer) ''')

    def check_if_exists(self):
        """ Checks if posts table exists. """

        self.cur.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='posts'")
        # Check if the table exists.
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            logger.error("Table does not exist in the database.")
            return False

    def insert_to_database(self, payload):
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
            print(row)
