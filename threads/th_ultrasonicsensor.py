import asyncio
import logging
import collections
import numpy as np
from library.messages.Message import Message
from config import WEBSOCKET_QUEUE
from library.observers.Observer import Observer
from library.ultrasonic.ultrasonicsensors import ultra_sonic_sensors
from library.messages.DistanceMessage import DistanceMessage
from controls.RoboControl import RoboControl
from library.queue.RoboQueue import RoboQueue
import queue

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ARRAY_MAX_LENGHT = 6
h_dist = collections.deque(maxlen=ARRAY_MAX_LENGHT)

# This Thread controls the ultrasonic sensor
async def th_ultrasonicsensor(robotControl:RoboControl, queues:RoboQueue):
    logger.warning("warm up ultrasonic sensor")
    while len(h_dist)<=ARRAY_MAX_LENGHT-1:
        h_dist.append(int(ultra_sonic_sensors[0].get_distance() *100))
        await asyncio.sleep(0.1)
    logger.warning("warm up completed")

    # register sensor observer in robot control
    ultrasonicSensorObserver = Observer()
    robotControl.register_observer(ultrasonicSensorObserver, robotControl.on_distance_sensor)

    # get queue to send ws message
    ws_queue: queue.Queue = queues.get(WEBSOCKET_QUEUE)
    # Loop and update network with distance and object direction
    while True:
        try:
             distance = ultra_sonic_sensors[0].get_distance()
             direction = calculate_obstacle_direction(distance)

             ultrasonicSensorObserver.emit =  DistanceMessage(True, distance,direction)

             ws_queue.put(Message("Alert", "ws_ultrasonic", {"enabled": True, "direction":direction, "distance": distance}))
             #webSocketQueue.put(Message("Alert", "ws_ultrasonic", {"enabled": True, "direction":direction, "distance": distance}))
    #         if distance<=0.2:
    #             #Prepare Message
    #             message = Message("Alert", "UltrasonicSensor-0", {"message":"obstacle in line", "distance": distance})
    #             jmessage = json.dumps(message.__dict__)
    #             await send_message_to_all(jmessage, WS_USERS)
    #             logger.warning("obstacle at %s cm direction %s" % (distance * 100, str(dev_dist)))
    #         else:
    #             logger.warning("distance %s cm, direction %s" % (distance * 100, str(dev_dist)))
             logger.warning("distance %s cm, direction %s" % (distance * 100, str(direction)))
        except ValueError:
             logger.error ("Error:" + ValueError)
             ultrasonicSensorObserver.emit = DistanceMessage(False, 0, 0)
        except TypeError:
             logger.error("Error:" + TypeError)
             ultrasonicSensorObserver.emit = DistanceMessage(False, 0, 0)
        await asyncio.sleep(2)

def calculate_obstacle_direction(distance):
    h_dist.append(int(distance * 100))
    splits = ARRAY_MAX_LENGHT - 1
    x = np.array(h_dist)
    output = [sum(x[i:i + splits]) / splits for i in range(len(x) - splits + 1)]
    dev_dist = np.diff(output, n=1)[0]
    direction = dev_dist / 100
    return direction