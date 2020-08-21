from gpiozero import Motor, OutputDevice
from library.motor.RoboMotor import RoboMotor

motors = []
motors_enable = []

# MOTOR 1
motors.insert(RoboMotor.ONE.value, Motor(24, 27, pwm=False))
motors_enable.insert(RoboMotor.ONE.value, OutputDevice(5, initial_value=1))

# MOTOR 2
motors.insert(RoboMotor.TWO.value, Motor(6, 22, pwm=False))
motors_enable.insert(RoboMotor.TWO.value, OutputDevice(17, initial_value=1) )

# MOTOR 3
motors.insert(RoboMotor.THREE.value, Motor(23, 16, pwm=False) )
motors_enable.insert(RoboMotor.THREE.value, OutputDevice(12, initial_value=1) )

# MOTOR 4
motors.insert(RoboMotor.FOUR.value, Motor(13, 18, pwm=False) )
motors_enable.insert(RoboMotor.FOUR.value, OutputDevice(25, initial_value=1) )


def enable_robomotor(robomotor: RoboMotor):
    motors_enable[robomotor.value] = OutputDevice(5, active_high=1)

def disable_robotmotor(robomotor: RoboMotor):
    motors_enable[robomotor.value] = OutputDevice(5, active_high=0)

def move_forward(speed:int, robomotor:RoboMotor):
    motors[robomotor.value].forward(speed)

def move_backward(speed:int, robomotor:RoboMotor):
    motors[robomotor.value].backward(speed)

def stop_robomotor(robomotor:RoboMotor):
    motors[robomotor.value].stop()

def reverse_robomotor(robomotor:RoboMotor):
    motors[robomotor.value].reverse()