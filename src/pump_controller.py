#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
from camera_controller import CameraController
from logzero import logger


class PumpController:
    """ Controls the pump motor """

    def __init__(self):
        self.cam = CameraController()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.set_gpio_pins()

    def set_gpio_pins(self):
        """ Set GPIO pins as output """
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        self.pwm = GPIO.PWM(7, 100)
        self.pwm.start(0)

    def run_pump_forward(self):
        """ Runs pump motor forward """

        self.cam.start_record()
        logger.info("Starting pump.")
        self.start_pump()
        # Set GPIO pins
        GPIO.output(3, False)
        GPIO.output(5, True)
        GPIO.output(7, True)

    def run_pump_backward(self):
        """ Runs pump motor backward """
        self.start_pump()
        GPIO.output(3, True)
        GPIO.output(5, False)

    def stop_pump(self):
        """ Stops pump and cleans up."""

        logger.info("Stopping pump.")
        GPIO.output(7, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop(0)
        GPIO.cleanup()
        self.cam.stop_record()

    def start_pump(self):
        """ Starts pump. """

        GPIO.output(7, True)
        self.pwm.ChangeDutyCycle(100)
