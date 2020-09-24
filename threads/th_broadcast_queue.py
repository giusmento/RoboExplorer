import asyncio
import json
import queue
import logging
from config import WEBSOCKET_QUEUE, LOG_FORMAT
from library.communication.WebSocketServer import WebSocketServer
from library.queue.RoboQueues import RoboQueues
from library.messages.Message import Message

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Broadcast messages in the queue WS_QUEUE
async def th_broadcast_queue(webSocketServer:WebSocketServer, roboQueues: RoboQueues):
    await_time = 1
    q:queue.Queue = roboQueues.get(WEBSOCKET_QUEUE)
    while True:
        if q.empty() is False:
            await send_all_enqueued_messages(q, webSocketServer)
            await_time = 1
        else:
            await_time = await_time + 0.5
        await asyncio.sleep(await_time)

async def send_all_enqueued_messages(q:queue.Queue, webSocketServer:WebSocketServer):
    while not q.empty():
        try:
            item = q.get()
            # TODO: check if item is a Message or throw error
            if isinstance(item, Message):
                #jmessage = json.dumps(item)
                jmessage = json.dumps(item.__dict__)
                await webSocketServer.broadcast(jmessage)
                q.task_done()
            else:
                logger.warning("item %s is not instance of Message" % item)
        except:
            logger.error("cant send item %s", item)