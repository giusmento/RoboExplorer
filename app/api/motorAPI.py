from flask import Blueprint

motor_api = Blueprint('motor_api', __name__)

@motor_api.route("/motor")
def motor():
    return "this is motor API"