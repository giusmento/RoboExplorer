from controls.RoboControl import RoboControl
from library.robot.RoboExplorer import RoboExplorer
import json

class RoboControl_EasyMove(RoboControl):

    def __init__(self, roboExplorer:RoboExplorer):
        super().__init__();
        self.roboExplorer = roboExplorer
        pass

    def on_distance_sensor(self, data):
        print("new data from distance sensor:" + str(data))

    def on_status(self):
        status = self.roboExplorer.status()
        return status