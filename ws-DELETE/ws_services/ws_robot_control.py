import asyncio
import json
import logging
from ws.messages.Message import Message
from ws.WebSocketServer import WS_USERS
#from library.robot.RobotExplorer import robotExplorer
from ws.utils.ws_utils import send_message_to_all

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Robot controller
async def ws_robot_control(roboExplorer):
    while True:
        # controlled variabled
        sensor_distance = roboExplorer.get_distance()
        motor_moving = roboExplorer.is_motors_moving()
        sensor_distance_direction = roboExplorer.distance_sensor_direction
        # Secure stop
        if(roboExplorer.is_ready()==False):
            logger.info("Robot not ready to move")
        elif(sensor_distance<0.2) & (motor_moving):
            logger.info("stop all motors")
            roboExplorer.stop_motors()
            message = Message("Control", "RobotContoller", {"action": "Stop all motors", "distance": sensor_distance})
            jj = json.dumps(message.__dict__)
            await send_message_to_all(jj, WS_USERS)
        # Start moving
        elif (sensor_distance>0.2) & (motor_moving==False):
            logger.info("start moving motors - speed: 10")
            roboExplorer.move_forward(10)
            message = Message("Control", "RobotContoller", {"action": "start moving", "speed": 10})
            jj = json.dumps(message.__dict__)
        # increase speed
        elif (motor_moving) & (sensor_distance_direction >=0):
            new_speed = roboExplorer.last_speed + (roboExplorer.max_speed/ 10)
            if(new_speed>roboExplorer.max_speed):
                new_speed= roboExplorer.max_speed
            roboExplorer.move_forward(new_speed)
            logger.info("increase motors speed: %s ", str(new_speed) )
            message = Message("Control", "RobotContoller", {"action": "increase speed", "speed": new_speed})
            jj = json.dumps(message.__dict__)
        # decrease speed
        elif (motor_moving) & (sensor_distance_direction < 0):
            new_speed = roboExplorer.last_speed - (roboExplorer.max_speed / 10)
            if (new_speed < 0):
                new_speed = 0
            roboExplorer.move_forward(new_speed)
            logger.info("decrease motors speed: %s ", str(new_speed))
            message = Message("Control", "RobotContoller", {"action": "increase speed", "speed": new_speed})
            jj = json.dumps(message.__dict__)
        await asyncio.sleep(1)
    # reset all pins
    roboExplorer.close()