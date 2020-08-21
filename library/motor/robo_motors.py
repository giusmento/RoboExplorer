from gpiozero import Motor, OutputDevice
from library.motor.RoboMotor import RoboMotor

motors = []
motors_enable = []

# MOTOR 1
motors[RoboMotor.ONE] = Motor(24, 27)
motors_enable[RoboMotor.ONE] = OutputDevice(5, initial_value=0)

# MOTOR 2
motors[RoboMotor.TWO] = Motor(6, 22)
motors_enable[RoboMotor.TWO] = OutputDevice(17, initial_value=0)

# MOTOR 3
motors[RoboMotor.THREE] = Motor(23, 16)
motors_enable[RoboMotor.THREE] = OutputDevice(12, initial_value=0)

# MOTOR 4
motors[RoboMotor.FOUR] = Motor(13, 18)
motors_enable[RoboMotor.FOUR] = OutputDevice(25, initial_value=0)


def enable_robomotor(robomotor: RoboMotor):
    motors_enable[robomotor] = OutputDevice(5, active_high=1)

def disable_robotmotor(robomotor: RoboMotor):
    motors_enable[robomotor] = OutputDevice(5, active_high=0)

def move_forward(speed:int, robomotor:RoboMotor):
    motors[robomotor].forward(speed)

def move_backward(speed:int, robomotor:RoboMotor):
    motors[robomotor].backward(speed)

def stop_robomotor(robomotor:RoboMotor):
    motors[robomotor].stop()

def reverse_robomotor(robomotor:RoboMotor):
    motors[robomotor].reverse()