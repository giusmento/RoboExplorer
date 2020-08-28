from library.motor.motors import RobotMotors
from library.ultrasonic.ultrasonicsensors import ultra_sonic_sensors

class RobotExplorer:
    def __init__(self):
        self.name= "Robot Explorer"
        self.max_speed = 100
        self.__motors = [RobotMotors[0], RobotMotors[1]]
        self.__ultrasonicsensor = ultra_sonic_sensors[0]
        self.collition_detection = True
        self.last_speed= 0
        self.is_moving = False
        self.distance_sensor_direction = 0
        self.distance_sensor_enabled = False

    def move_forward(self, speed):
        if speed is None:
            speed = self.last_speed
        else:
            self.last_speed= speed

        self.is_moving = True
        self.__motors[0].forward(speed/self.max_speed)
        self.__motors[1].forward(speed/self.max_speed)

    def stop_motors(self):
        self.last_speed = 0
        self.__motors[0].stop()
        self.__motors[1].stop()
        self.is_moving = False

    def get_distance(self):
        distance = self.__ultrasonicsensor.get_distance()
        return distance

    def is_motors_moving(self):
        return self.is_moving

    def status(self):
        return {"last_distance": self.__ultrasonicsensor.last_distance }

    def is_ready(self):
        return self.distance_sensor_enabled

    def close(self):
        self.__motors[0].close()
        self.__motors[1].close()
        self.__ultrasonicsensor.close()

robotExplorer = RobotExplorer()