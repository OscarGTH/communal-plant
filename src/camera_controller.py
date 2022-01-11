from pathlib import Path
from datetime import datetime
from subprocess import call
from logzero import logger
import picamera


# Video file path
VIDEO_PATH = str(Path().resolve()) + "/videos/"

class CameraController:


    def __init__(self) -> None:
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.video_file_path = VIDEO_PATH + datetime.now().date()
    
    def record(self, duration):
        """ Starts recording video for a given duration. """

        try:
            logger.info("Starting to record video.")
            # Start recording video.
            self.camera.start_recording(self.video_file_path + ".h264")
            logger.info("Recording for " + str(duration) + " seconds.")
            # Record for the given duration.
            self.camera.wait_recording(duration)
            # Stop recording.
            self.camera.stop_recording()
            logger.info("Sleeping for 5 seconds to wait for the file.")
            return self.convert_recording_to_mp4()
        except Exception as ex:
            logger.warning("Error happened while recording video.")
            logger.error(ex)
        

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
            return True
        except:
            logger.error("Error when converting video to mp4.")
            return False

