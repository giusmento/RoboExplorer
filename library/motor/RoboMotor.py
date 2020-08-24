from gpiozero import Motor, OutputDevice
import gpiozero

class RoboMotor:
    def __init__(self, name, enable, positive, negative):
        self.motor: Motor = Motor(positive, negative, pwm=True, pin_factory= gpiozero.Device.pin_factory)
        self.motorEnable:OutputDevice = OutputDevice(enable, active_high=0)
        self.speed = 0
        self.name = name
        self.active = False

    def forward(self, speed=1):
        self.motor.forward(speed)
        self.speed = speed

    def stop(self):
        self.motor.stop()
        self.speed = 0

    def backward(self, speed=1):
        self.motor.backward(speed)
        self.speed = speed * (-1)

    def reverse(self):
        self.motor.reverse()
        self.speed = self.speed * (-1)

    def enable(self):
        self.motorEnable.off()
        self.active = True

    def disable(self):
        self.motorEnable.on()
        self.active = False

    def is_active(self):
        return self.active

    def get_speed(self):
        return self.speed