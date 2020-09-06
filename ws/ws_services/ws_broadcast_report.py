import asyncio
import json
from ws.messages.Message import Message
from ws.WebSocketServer import WS_USERS
#from library.robot.RobotExplorer import robotExplorer
from ws.utils.ws_utils import send_message_to_all

# Broadcast robot sensors info
# RobotSensorInfo
async def ws_broadcast_report(roboExplorer):
    while True:
        payload = roboExplorer.status()
        message = Message("Summary", "RobotExplorer", payload)
        jj = json.dumps(message.__dict__)
        await send_message_to_all(jj, WS_USERS)
        # await asyncio.gather(
        #     *[ws.send(jj) for ws in WS_USERS],
        #     return_exceptions=False,
        # )
        await asyncio.sleep(5)