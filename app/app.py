from flask import Flask, render_template
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from api.motorAPI import motor_api

application = Flask(__name__)

application.register_blueprint(motor_api)

@application.route('/')
def hello():
    return render_template("home.html", value= "test")

if __name__ == '__main__':
    application.run()