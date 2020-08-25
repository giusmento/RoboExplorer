from gpiozero import DistanceSensor

class RoboUltraSonic:

    def __init__(self, echo, trigger):
        self.echo_pin = echo
        self.trigger_pin = trigger
        self.max_distance = 2
        self.unit = "meter"
        self.threshold_distance = 0.1
        self.sensor = DistanceSensor(
                echo=self.echo_pin,
                trigger=self.trigger_pin,
                threshold_distance= self.threshold_distance,
                max_distance=self.max_distance
        )

    def get_distance(self):
        return self.sensor.distance
