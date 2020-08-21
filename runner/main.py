import logging
from logging.config import fileConfig
import argparse
from os import path
import sys
import os

import gpiozero
from gpiozero.pins.mock import MockFactory, MockPWMPin

# Parse args
parser = argparse.ArgumentParser(description='Exercise')
parser.add_argument('--mock_gpio', type=bool, nargs='?', const=True, default=False, help='Mock gpio', required=False)
parser.add_argument('--demo', type=bool, nargs='?', const=True, default=False, help='start demo', required=False)

args = parser.parse_args()
MOCK_GPIO = args.mock_gpio if args.mock_gpio != None else False
DEMO = args.demo if args.demo != None else False

if MOCK_GPIO:
    gpiozero.Device.pin_factory = MockFactory(pin_class=MockPWMPin)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from application.demo import demo_robo_explorer

#logger
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info('Application just started.')

    if DEMO:
        logger.info('Start demo')
        demo_robo_explorer()
    else:
        logger.info('nothing to do yet!')

    logger.info('exit!')
