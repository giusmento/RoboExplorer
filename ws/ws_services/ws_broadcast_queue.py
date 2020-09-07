import asyncio
import json
import queue
from ws.WebSocketServer import WebSocketServer
from library.queue.RoboQueue import RoboQueue

WS_QUEUE = "ws-sendMessage"
# Broadcast messages in the queue WS_QUEUE
async def ws_broadcast_queue(roboQueue: RoboQueue, webSocketServer:WebSocketServer):
    await_time = 1
    q:queue.Queue = roboQueue.get(WS_QUEUE)
    while True:
        if q.empty() is False:
            await send_all_enqueued_messages(q, webSocketServer)
            await_time = 1
        else:
            await_time = await_time + 0.5
        await asyncio.sleep(await_time)

async def send_all_enqueued_messages(q:queue.Queue, webSocketServer:WebSocketServer):
    while not q.empty():
        item = q.get()
        jmessage = json.dumps(item.__dict__)
        await webSocketServer.broadcast(jmessage)
        print(f'Working on {item}')
        q.task_done()