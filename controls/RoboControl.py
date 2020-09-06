from abc import ABC, abstractmethod
from library.robot.RoboExplorer import RoboExplorer
from library.abstracts.RegistrableClass import RegistrableClass

class RoboControl( RegistrableClass, ABC):

    def __init__(self):
        #self.observers = []
        # self.sensorObserver = sensorObserver
        # self.sensorObserver.bind_to(self.on_distance_sensor)
        self.roboExplorer = RoboExplorer()
        super().__init__()

    @abstractmethod
    def on_distance_sensor(self, data):
        pass

    # def register_observer(self, sensorObserver, callback):
    #     self.observers.append(sensorObserver)
    #     self.observers[len(self.observers)-1].bind_to(callback)