import logging
from logging.config import fileConfig
from os import path
import time
import sys
import os

import gpiozero
from gpiozero.pins.mock import MockFactory

gpiozero.Device.pin_factory = MockFactory()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from library.motor.RoboMotor import RoboMotor
from library.motor import robo_motors

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info('Application just started.')

    #robo_motors.enable_robomotor(RoboMotor.ONE)
    robo_motors.move_forward(1, RoboMotor.ONE)
    time.sleep(1)
    robo_motors.stop_robomotor(RoboMotor.ONE)

    logger.info('exit!')
