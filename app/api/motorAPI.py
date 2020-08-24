from flask import Blueprint, jsonify, Response, make_response, request
from flask import current_app
import json
import random
from library.motor.motors import RobotMotors

motor_api = Blueprint('motor_api', __name__)

@motor_api.route("/motors/<int:motor_id>/status", methods=['GET'])
def get_motor_status(motor_id):
    if int(motor_id) > 4:
        response = make_response(jsonify(error="error"), 403)
    else:
        # get status
        enabled = RobotMotors[motor_id].is_active()
        speed = RobotMotors[motor_id].get_speed() * 10
        response = Response(
        json.dumps({'enabled': enabled, 'speed': speed }),
        status=200,
        mimetype='application/json'
        )
    return response

@motor_api.route("/motors/<int:motor_id>", methods=['POST'])
def put_motor_speed(motor_id):
    if not request.json:
        return Response(
            "data is not is JSON format",
            status=505,
            mimetype='application/json'
        )
    if 'speed' in request.json:
        current_app.logger.info("Set speed to " + str(request.json['speed']))
        try:
            #RobotMotorsOne.forward(request.json['speed']/10)
            RobotMotors[motor_id].forward(request.json['speed']/10)
        except ValueError as e:
            return Response(
                e.args[0],
                status=500,
                mimetype='application/json'
            )
    if 'enabled' in request.json:
        current_app.logger.info("Set enable to " + str(request.json['enabled']))
        try:
            if request.json['enabled']:
                RobotMotors[motor_id].enable()
            else:
                RobotMotors[motor_id].disable()
        except ValueError as e:
            return Response(
                e.args[0],
                status=500,
                mimetype='application/json'
            )
    return Response(
        "OK",
        status=200,
        mimetype='application/json'
        )