import asyncio
import logging
import queue
from config import BROADCAST_STATUS_TIME
from controls.RoboControl import RoboControl
from config import LOG_FORMAT
from library.observers.Observer import Observer

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Broadcast robot status
async def th_broadcast_robo_status(roboControl:RoboControl):

    summary_observer = Observer()
    roboControl.register_receiver(summary_observer, roboControl.on_status)

    while True:
        logger.debug("ws_broadcast_report")
        test = summary_observer.receive()
        logger.debug(test)
        await asyncio.sleep(BROADCAST_STATUS_TIME)