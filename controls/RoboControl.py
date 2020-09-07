from abc import ABC, abstractmethod
from library.robot.RoboExplorer import RoboExplorer
from library.abstracts.RegistrableClass import RegistrableClass

class RoboControl( RegistrableClass, ABC):

    def __init__(self):
        self.roboExplorer = RoboExplorer()
        super().__init__()

    @abstractmethod
    def on_distance_sensor(self, data):
        pass