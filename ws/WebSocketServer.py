#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import datetime
import random
import queue
from ws.config import *
from ws.messages.Message import Message

#from library.robot.RobotExplorer import robotExplorer



class WebSocketServer(object):
    def __init__(self):
        self.WS_USERS = set()
        self.ws = None
        self.welcome_message = "Connected to RoboExplorer websocket"
        self.__queue = queue.Queue()
        super().__init__()

    def start(self, HOST_ADDRESS, HOST_PORT):
        self.ws = websockets.serve(self.__ws_main, HOST_ADDRESS, HOST_PORT)
        return self.ws

    async def send(self):
        pass

    async def broadcast(self, message):
        if self.WS_USERS:  # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.WS_USERS])

    def enqueue_message(self,message):
        self.__queue.put(message)

    async def send_all_enqueued_messages(self):
        while not self.__queue.empty():
            item = self.__queue.get()
            jmessage = json.dumps(item.__dict__)
            await self.broadcast(jmessage)
            print(f'Working on {item}')
            self.__queue.task_done()

    async def is_queue_empty(self):
        return self.__queue.empty()

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



STATE = {"value": 0}

WS_USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def generate_welcome_event():
    #return json.dumps({"type": "users", "count": len(USERS)})
    return json.dumps("Connected to RoboExplorer websocket")


async def notify_state():
    if WS_USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in WS_USERS])


async def notify_users():
    if WS_USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps("New user connected")
        await asyncio.wait([user.send(message) for user in WS_USERS])


async def register_new_user(websocket):
    WS_USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    WS_USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register_new_user(websocket)
    try:
        await websocket.send(generate_welcome_event())
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)
        async for message in websocket:
            try:
                data = json.loads(message)
                if data["action"] == "minus":
                    STATE["value"] -= 1
                    await notify_state()
                elif data["action"] == "plus":
                    STATE["value"] += 1
                    await notify_state()
                else:
                    logging.error("unsupported event: {}", data)
            except:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        await unregister(websocket)

start_ws_server = websockets.serve(counter, HOST_ADDRESS, HOST_PORT)

