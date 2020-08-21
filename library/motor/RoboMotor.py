from gpiozero import Motor, OutputDevice
import gpiozero

class RoboMotor:
    def __init__(self, enable, positive, negative):
        self.motor: Motor = Motor(positive, negative, pwm=True, pin_factory= gpiozero.Device.pin_factory)
        self.motorEnable:OutputDevice = OutputDevice(enable, active_high=0)

    def forward(self, speed=1):
        self.motor.forward(speed)

    def stop(self):
        self.motor.stop()

    def backward(self, speed=1):
        self.motor.backward(speed)

    def reverse(self):
        self.motor.reverse()

    def enable(self):
        self.motorEnable.on()

    def disable(self):
        self.motorEnable.off()

    def is_active(self):
        return self.motor.is_active