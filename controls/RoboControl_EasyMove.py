from controls.RoboControl import RoboControl
import json

class RoboControl_EasyMove(RoboControl):

    def __init__(self,):
        super().__init__();
        pass


    def on_distance_sensor(self, data):
        print("new data from distance sensor:" + str(data))