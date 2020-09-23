from abc import ABC, abstractmethod
from library.robot.RoboExplorer import RoboExplorer
from library.abstracts.RegistrableClass import RegistrableClass

class RoboControl(RegistrableClass, ABC):

    def __init__(self):
        self.roboExplorer = RoboExplorer()
        super().__init__()

    @abstractmethod
    def on_distance_sensor(self, data):
        pass

    @abstractmethod
    def on_motor_increase(self, data):
        pass

    @abstractmethod
    def on_motor_decrease(self, data):
        pass

    @abstractmethod
    def on_motor_stop(self):
        pass

    @abstractmethod
    def get_camera_status(self):
        pass

    @abstractmethod
    def on_status(self):
        pass