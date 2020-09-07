import time
import logging
from library.motor.motors import RobotMotors

logger = logging.getLogger()

def demo_robo_explorer():

    logger.info("Motor One move forward")
    RobotMotors[1].forward()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotors[1].stop()
    time.sleep(1)
    logger.info("Motor One move backward")
    RobotMotors[1].backward()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotors[1].stop()
    time.sleep(1)
    logger.info("Motor One move forward half speed")
    RobotMotors[1].forward(0.5)
    time.sleep(2)
    logger.info("Motor One move reverse")
    RobotMotors[1].reverse()
    time.sleep(2)
    logger.info("Motor One move stop")
    RobotMotors[1].stop()

if __name__ == "__main__":
    demo_robo_explorer()