import logging
from logging.config import fileConfig
import argparse
from os import path
import time
import sys
import os

import gpiozero
from gpiozero.pins.mock import MockFactory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from library.motor.motors import RobotMotorOne

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info('Application just started.')

    parser = argparse.ArgumentParser(description='Exercise')
    parser.add_argument('--mock_gpio', type=bool, nargs='?', const=True, default=False, help='Mock gpio', required=False)

    args = parser.parse_args()
    MOCK_GPIO = args.test if args.test != None else False

    if MOCK_GPIO:
        gpiozero.Device.pin_factory = MockFactory()

    
    RobotMotorOne.forward()
    time.sleep(5)
    RobotMotorOne.stop()
    logger.info('exit!')
