from flask import Blueprint, jsonify, Response, make_response, request
import json
from library.ultrasonic.ultrasonicsensors import ultra_sonic_sensors
distance_api = Blueprint('distance_api', __name__)

@distance_api.route("/distances/<int:sensor_id>/status", methods=['GET'])
def get_motor_status(sensor_id):
    distance = ultra_sonic_sensors[sensor_id].get_distance()
    max_distance = ultra_sonic_sensors[sensor_id].max_distance
    response = Response(
    json.dumps({'distance': distance, 'max_distance': max_distance }),
    status=200,
    mimetype='application/json'
    )
    return response