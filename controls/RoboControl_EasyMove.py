from controls.RoboControl import RoboControl
from library.robot.RoboExplorer import RoboExplorer

class RoboControl_EasyMove(RoboControl):

    def __init__(self, roboExplorer:RoboExplorer):
        super().__init__();
        self.roboExplorer = roboExplorer
        pass

    def on_distance_sensor(self, data):
        print("new data from distance sensor:" + str(data))
        # when direction smaller than zero - decrease speed
        if data.direction > 0:
            self.roboExplorer.increase_speed(0)
        else:
            self.roboExplorer.decrease_speed(0)
        # when direction bigger than zero - increase speed
    def on_motor_increase(self, data):
        self.roboExplorer.increase_speed(data)

    def on_motor_decrease(self, data):
        self.roboExplorer.decrease_speed(data)

    def on_motor_stop(self):
        self.roboExplorer.stop_motors()

    def get_camera_status(self):
        return self.roboExplorer.camera

    def on_status(self):
        status = self.roboExplorer.status()
        return status