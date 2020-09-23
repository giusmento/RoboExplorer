import asyncio
import logging
import queue
from config import WEBSOCKET_QUEUE
from controls.RoboControl import RoboControl
from config import LOG_FORMAT
from library.observers.Observer import Observer
from library.queue.RoboQueue import RoboQueue
from library.messages.Message import Message

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Broadcast robot status
async def th_broadcast_robo_status(roboControl:RoboControl, roboQueue:RoboQueue):

    summary_observer = Observer()
    roboControl.register_receiver(summary_observer, roboControl.on_status)
    ws_queue: queue.Queue = roboQueue.get(WEBSOCKET_QUEUE)

    while True:
        print("ws_broadcast_report")
        test = summary_observer.receive()
        ws_queue.put(Message("Summary", "all", "robot_status", test))
        print(test)
        ws_queue.put(test)
        await asyncio.sleep(5)