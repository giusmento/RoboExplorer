import asyncio
import logging
from controls.RoboControl import RoboControl
from config import LOG_FORMAT

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Broadcast robot status
async def th_broadcast_robo_status(roboControl:RoboControl):
    while True:
        print("ws_broadcast_report")
        # payload = roboExplorer.status()
        # message = Message("Summary", "RobotExplorer", payload)
        # jj = json.dumps(message.__dict__)
        # await send_message_to_all(jj, WS_USERS)
        # # await asyncio.gather(
        # #     *[ws.send(jj) for ws in WS_USERS],
        # #     return_exceptions=False,
        # # )
        await asyncio.sleep(5)