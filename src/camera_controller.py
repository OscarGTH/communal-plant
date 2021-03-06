from pathlib import Path
from datetime import datetime
import time
from subprocess import call
import os
from logzero import logger
import picamera


# Video file path
VIDEO_PATH = str(Path().resolve()) + "/videos/"
IMAGE_PATH = str(Path().resolve()) + "/images/"


class CameraController:

    def __init__(self) -> None:
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1296, 730)
        self.video_file_path = VIDEO_PATH + str(datetime.now().date())
        self.image_file_path = IMAGE_PATH + str(time.time())

    def start_record(self):
        """ Starts to record video. """

        try:
            # Delete possible video that was taken earlier.
            logger.info("Deleting previous video if exists.")
            self.delete_previous_video()
            logger.info("Starting to record video.")
            # Start recording video.
            self.camera.start_recording(self.video_file_path + ".h264")
        except Exception as ex:
            logger.warning("Error happened while recording video.")
            logger.error(ex)

    def stop_record(self):
        """ Stops video recording and calls converter function. """

        try:
            logger.info("Stopping video recording.")
            # Stop recording.
            self.camera.stop_recording()
            # Take a picture of the plant.
            self.capture_image()
            # Convert video to mp4 and return result.
            return self.convert_recording_to_mp4()
        except Exception as ex:
            logger.warning("Error happened ending video recording.")
            logger.error(ex)

    def capture_image(self):
        """ Captures single image for later use. """

        logger.info("Capturing image.")
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        # Capture image.
        self.camera.capture(self.image_file_path + ".png")
        logger.info("Image captured.")

    def convert_recording_to_mp4(self):
        """ Converts .h264 to mp4 file. """

        # Define file names of original and converted versions.
        orig_file = self.video_file_path + ".h264"
        converted_file = self.video_file_path + ".mp4"
        # Try to convert video with shell command.
        try:
            command = "MP4Box -add " + orig_file + " " + converted_file
            logger.info("Converting video to mp4.")
            # Execute command to convert h246 to mp4.
            call([command], shell=True)
            logger.info("Video successfully converted.")
            self.delete_original_format()
            return True
        except:
            logger.error("Error when converting video to mp4.")
            return False

    def delete_original_format(self):
        """ Deletes the H246 format file after conversion to mp4. """

        orig_file = Path(self.video_file_path + '.h264')
        # Check if file exists.
        if orig_file.is_file():
            # Remove file.
            os.remove(self.video_file_path + ".h264")

    def delete_previous_video(self):
        """ Deletes possibly existing mp4 video with the same date. """

        converted_file = Path(self.video_file_path + '.mp4')
        # Check if file exists.
        if converted_file.is_file():
            # Remove file.
            os.remove(self.video_file_path + ".mp4")
