#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import datetime
import random
from ws.config import *
from ws.messages.Message import Message
from library.robot.RobotExplorer import robotExplorer

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
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    except KeyboardInterrupt:
        pass
    finally:
        await unregister(websocket)

start_ws_server = websockets.serve(counter, HOST_ADDRESS, HOST_PORT)

