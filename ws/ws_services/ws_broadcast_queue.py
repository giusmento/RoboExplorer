import asyncio
import json
import queue
from ws.WebSocketServer import WebSocketServer
# Broadcast robot sensors info
# RobotSensorInfo
async def ws_broadcast_queue(webQueue: queue.Queue, webSocketServer:WebSocketServer):
    await_time = 1
    while True:
        if await    webSocketServer.is_queue_empty() is False:
            await webSocketServer.send_all_enqueued_messages()
            await_time = 1
        else:
            await_time = await_time + 0.5
        await asyncio.sleep(await_time)