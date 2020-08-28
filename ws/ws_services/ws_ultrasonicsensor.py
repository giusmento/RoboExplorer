import asyncio
import json
import logging
import collections
import numpy as np
from ws.messages.Message import Message
from ws.WebSocketServer import WS_USERS
from library.robot.RobotExplorer import robotExplorer
from ws.utils.ws_utils import send_message_to_all

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Broadcast robot sensors info
# RobotSensorInfo
async def ws_ultrasonicsensor():
    ARRAY_MAX_LENGHT = 6
    h_dist = collections.deque(maxlen=ARRAY_MAX_LENGHT)
    logger.warning("warm up ultrasonic sensor")
    while len(h_dist)<=ARRAY_MAX_LENGHT-1:
        h_dist.append(int(robotExplorer.get_distance() *100))
        await asyncio.sleep(0.1)
    logger.warning("warm up completed")
    robotExplorer.distance_sensor_enabled= True
    while True:
        try:
            distance = robotExplorer.get_distance()
            h_dist.append(int(distance*100))
            splits = ARRAY_MAX_LENGHT - 1
            x = np.array(h_dist)
            output = [sum(x[i:i + splits]) / splits for i in range(len(x) - splits + 1)]
            dev_dist = np.diff(output, n=1)[0]
            robotExplorer.distance_sensor_direction = dev_dist/100
            if distance<=0.2:
                #Prepare Message
                message = Message("Alert", "UltrasonicSensor-0", {"message":"obstacle in line", "distance": distance})
                jmessage = json.dumps(message.__dict__)
                await send_message_to_all(jmessage, WS_USERS)
                logger.warning("obstacle at %s cm direction %s" % (distance * 100, str(dev_dist)))
            else:
                logger.warning("distance %s cm, direction %s" % (distance * 100, str(dev_dist)))
        except ValueError:
            print ("Error:" + ValueError)
            robotExplorer.distance_sensor_enabled = False
        except TypeError:
            robotExplorer.distance_sensor_enabled = False
        await asyncio.sleep(2)