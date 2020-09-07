from gpiozero import DistanceSensor
from utils.parse_args import MOCK_GPIO, PIGPIO_ADDR
import random

class RoboUltraSonic:

    def __init__(self, echo, trigger):
        self.echo_pin = echo
        self.trigger_pin = trigger
        self.max_distance = 2
        self.last_distance = 0.5 * self.max_distance
        self.unit = "meter"
        self.threshold_distance = 0.1
        self.sensor = DistanceSensor(
                echo=self.echo_pin,
                partial=True,
                trigger=self.trigger_pin,
                threshold_distance= self.threshold_distance,
                max_distance=self.max_distance
        )

    def get_distance(self):
        try:
            if (MOCK_GPIO) & (PIGPIO_ADDR is None):
                self.last_distance = self.__simulate_distance()
                return self.last_distance
            else:
                self.last_distance = self.sensor.distance
                return self.last_distance
        except ValueError:
            print("Error get distance")

    def __simulate_distance(self):
        rand = random.randrange(-6, 8, 1)
        if(rand==0):
         return self.last_distance
        if(abs(rand)> 4):
            pre = self.last_distance + (rand / 20)
            if pre < 0:
                pre = 0
            if pre> self.max_distance:
                pre = self.max_distance
            self.last_distance = pre
            return pre
        if(abs(rand)>0 & abs(rand)<=4):
            pre = self.last_distance + (rand / 100)
            if pre < 0:
                pre = 0
            if pre> self.max_distance:
                pre = self.max_distance
            self.last_distance = pre
            return pre

    def close(self):
        self.sensor.close()