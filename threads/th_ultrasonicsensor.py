import asyncio
import logging
import collections
import numpy as np
from config import ULTRASONIC_FETCH_TIME, LOG_LEVEL, LOG_FORMAT
from library.observers.Observer import Observer
from library.ultrasonic.ultrasonicsensors import ultra_sonic_sensors
from library.events.DistanceEvent import DistanceEvent
from controls.RoboControl import RoboControl

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

ARRAY_MAX_LENGHT = 6
h_dist = collections.deque(maxlen=ARRAY_MAX_LENGHT)

# This Thread controls the ultrasonic sensor
async def th_ultrasonicsensor(robotControl:RoboControl):
    logger.warning("warm up ultrasonic sensor")
    while len(h_dist)<=ARRAY_MAX_LENGHT-1:
        h_dist.append(int(ultra_sonic_sensors[0].get_distance() *100))
        await asyncio.sleep(0.1)
    logger.warning("warm up completed")

    # register sensor observer in robot control
    ultrasonicSensorObserver = Observer()
    robotControl.register_observer(ultrasonicSensorObserver, robotControl.on_distance_sensor)

    # Loop and update network with distance and object direction
    while True:
        try:
            distance = ultra_sonic_sensors[0].get_distance()
            direction = calculate_obstacle_direction(distance)

            ultrasonicSensorObserver.emit =  DistanceEvent(True, distance, direction)

        except ValueError:
             logger.error ("Error:" + ValueError)
             ultrasonicSensorObserver.emit = DistanceEvent(False, 0, 0)
        except TypeError:
             logger.error("Error:" + TypeError)
             ultrasonicSensorObserver.emit = DistanceEvent(False, 0, 0)
        await asyncio.sleep(ULTRASONIC_FETCH_TIME)

def calculate_obstacle_direction(distance):
    h_dist.append(int(distance * 100))
    splits = ARRAY_MAX_LENGHT - 1
    x = np.array(h_dist)
    output = [sum(x[i:i + splits]) / splits for i in range(len(x) - splits + 1)]
    dev_dist = np.diff(output, n=1)[0]
    direction = dev_dist / 100
    return direction