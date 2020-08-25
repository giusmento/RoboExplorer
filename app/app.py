from flask import Flask, render_template
import sys
import os
import argparse
import logging
from logging.config import fileConfig
from gpio_conf import gpio_conf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Parse args
parser = argparse.ArgumentParser(description='Exercise')
parser.add_argument('--pigpio_addr', type=str, help='Set host of remote gpio', required=False)
parser.add_argument('--mock_gpio', type=bool, nargs='?', const=True, default=False, help='Mock gpio', required=False)

args = parser.parse_args()

MOCK_GPIO = args.mock_gpio if args.mock_gpio != None else False
PIGPIO_ADDR = args.pigpio_addr if args.pigpio_addr != None else None

gpio_conf(MOCK_GPIO, PIGPIO_ADDR)

# LOAD ROBOT APIs
from api.motorAPI import motor_api
from api.distance_sensors_api import distance_api

# Start application
application = Flask(__name__)

# Load configuration file
if os.path.exists("config_file_default.cfg"):
    application.config.from_pyfile('config_file_default.cfg')

# Load blueprints
application.register_blueprint(motor_api)
application.register_blueprint(distance_api)

# configure logger
logging.config.fileConfig( 'logging_config.ini')

@application.route('/')
def hello():
    return render_template("home.html", value= "test")

if __name__ == '__main__':
    print("Welcome to " + application.config['APP_NAME']);
    application.run()