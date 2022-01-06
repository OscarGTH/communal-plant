#!/usr/bin/env python3

from datetime import datetime
from parse_config import get_configuration
from video_uploader import VideoUploader
# TODO: Uncomment this when run on RPi
# from pump_controller import PumpController
from graph_handler import GraphHandler
from db_handler import DatabaseHandler
from logzero import logger


class DailyProcess():

    def __init__(self, args) -> None:
        self.args = args
        # Initialize helper objects.
        self.dbh = DatabaseHandler(args)
        self.video_uploader = VideoUploader(args)
        self.graph_handler = GraphHandler(args)
        # TODO: Uncomment this when run on RPi
        #self.pump_controller = PumpController()

    def start_process(self):
        # Check if it isn't first post.
        if not self.dbh.is_first_post():
            logger.info("Performing normal daily process.")
            # Run common process that handles watering and posting.
            self.run_common_process()
        else:
            logger.info("Performing first posting process.")
            # Create first entry to database.
            self.create_first_entry()
            self.run_common_process()
        self.dbh.cleanup()

    def create_first_entry(self):
        """ Creates first database entry. """

        logger.info("Creating database entry for the first post.")
        # Get current date
        date = datetime.now().date()
        # Payload contains date, water amount and vote_count.
        payload = {'date': date, 'water_amount': 25, 'vote_count': 0}
        # Create table if needed.
        self.dbh.setup_table()
        # Inserting payload to table.
        self.dbh.insert_to_table(payload)

    def run_common_process(self):
        """ Common process that runs the watering and posting processes. """

        # If watering process succeeded, continue to posting process.
        if self.run_watering_process():
            logger.info("Continuing to uploading process.")
            self.run_upload_process()
        else:
            logger.error("Error happened while running watering process.")

    def run_upload_process(self):
        """ Uploads recorded video to File.io and sends it to Instagram. """

        logger.info("Running upload process.")
        # Get url to uploaded video.
        video_url = self.video_uploader.upload_video()
        if video_url:
            logger.info("Video url is: " + video_url)
            media_dict = self.graph_handler.start_posting_process(video_url)
            logger.info(media_dict)
            if 'id' in media_dict:
                logger.info("Updating media id to database.")
                # Update media id to database post entry.
                self.dbh.update_media_id(
                    media_dict['id'], datetime.now().date())
                self.dbh.get_all()

    def run_watering_process(self):
        """ Runs plant watering process. """

        success = True
        logger.info("Watering plant.")
        return success


def main():
    """ Main entry point of the app """

    # Get configuration
    args = get_configuration()
    daily = DailyProcess(args)
    daily.start_process()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
