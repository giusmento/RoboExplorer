from library.messages.Message import Message
from controls.RoboControl import RoboControl
import json

def ParseMessage(message:Message, roboControl:RoboControl):
    if message.get_type()=='setcommand':
        # Parse payload
        payload = json.loads(message.get_payload())
        if payload['device']=='motor':
            if payload['action']=='increase':
                roboControl.on_motor_increase(payload['value'])
            elif payload['action']=='decrease':
                roboControl.on_motor_decrease(payload['value'])
            elif payload['action']=='stop':
                roboControl.on_motor_stop()
        else:
            pass
