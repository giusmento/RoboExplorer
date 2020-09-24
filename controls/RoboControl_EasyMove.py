from controls.RoboControl import RoboControl
from library.robot.RoboExplorer import RoboExplorer
from library.queue.RoboQueues import RoboQueues
from config import WEBSOCKET_QUEUE, LOG_FORMAT, LOG_LEVEL
from library.messages.Message import Message
from library.events.DistanceEvent import DistanceEvent
import logging

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class RoboControl_EasyMove(RoboControl):

    def __init__(self, roboExplorer:RoboExplorer, roboQueues:RoboQueues):
        super().__init__();
        self.roboExplorer = roboExplorer
        self.roboQueues = roboQueues
        pass

    def on_distance_sensor(self, data:DistanceEvent):
        #print("new data from distance sensor:" + str(data))
        self.roboExplorer.distance_sensor_direction = data.direction
        self.roboExplorer.distance_sensor_last_distance = data.distance * 100
        self.roboExplorer.distance_sensor_enabled = data.enabled
        if data.distance<=0.3:
            self.roboExplorer.stop_motors()
            logger.warning("Motors stopped on distance event - dist:%s"% data.distance*100)
        # decrease or increase speed
        elif (data.distance>0.3 and data.direction>0):
            self.roboExplorer.increase_speed(0)
        else:
            self.roboExplorer.decrease_speed(0)
        # send robo update
        self.roboQueues.get(WEBSOCKET_QUEUE).put(Message("UPDATE", "all", "robot_status", self.roboExplorer.status()))
        logger.debug("Distance sensor updated dist: %s, dire: %s" % (data.distance * 100, data.direction))

    def on_motor_increase(self, data):
        self.roboExplorer.increase_speed(data)
        self.roboQueues.get(WEBSOCKET_QUEUE).put(Message("UPDATE", "all", "robot_status", self.roboExplorer.status_motors()))

    def on_motor_decrease(self, data):
        self.roboExplorer.decrease_speed(data)
        self.roboQueues.get(WEBSOCKET_QUEUE).put(Message("UPDATE", "all", "robot_status", self.roboExplorer.status_motors()))

    def on_motor_stop(self):
        self.roboExplorer.stop_motors()
        self.roboQueues.get(WEBSOCKET_QUEUE).put(Message("UPDATE", "all", "robot_status", self.roboExplorer.status_motors()))

    def get_camera_status(self):
        return self.roboExplorer.camera

    def on_status(self):
        status = self.roboExplorer.status()
        self.roboQueues.get(WEBSOCKET_QUEUE).put(Message("UPDATE", "all", "robot_status", self.roboExplorer.status_motors()))
        return status