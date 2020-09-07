#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import random
from config import LOG_FORMAT

logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WebSocketServer(object):
    def __init__(self):
        self.WS_USERS = set()
        self.ws = None
        self.welcome_message = "Connected to RoboExplorer websocket"
        super().__init__()

    def start(self, HOST_ADDRESS, HOST_PORT):
        # START BROADCAST
        logger.info("start web socket at " + HOST_ADDRESS + ":" + str(HOST_PORT))
        self.ws = websockets.serve(self.__ws_main, HOST_ADDRESS, HOST_PORT)
        return self.ws

    async def send(self, message):
        self.broadcast(message)

    async def broadcast(self, message):
        if self.WS_USERS:  # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.WS_USERS])

    async def __ws_main(self, websocket, path   ):
        await self.__register_new_user(websocket)
        try:
            await websocket.send(json.dumps(self.welcome_message))
            await asyncio.sleep(random.random() * 3)
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(data)
                except:
                    pass
        except KeyboardInterrupt:
            pass
        finally:
            await self.__unregister(websocket)

    async def __register_new_user(self, websocket):
        self.WS_USERS.add(websocket)

    async def __unregister(self, websocket):
        self.WS_USERS.remove(websocket)