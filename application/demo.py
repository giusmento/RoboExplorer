import time
import logging
from library.motor.motors import RobotMotorOne

logger = logging.getLogger()

def demo_robo_explorer():

    logger.info("Motor One move forward")
    RobotMotorOne.forward()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotorOne.stop()
    time.sleep(1)
    logger.info("Motor One move backward")
    RobotMotorOne.backward()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotorOne.stop()
    time.sleep(1)
    logger.info("Motor One move forward half speed")
    RobotMotorOne.forward(0.5)
    time.sleep(2)
    logger.info("Motor One move reverse")
    RobotMotorOne.reverse()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotorOne.stop()

if __name__ == "__main__":
    demo_robo_explorer()