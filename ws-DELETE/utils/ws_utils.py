import asyncio

async def send_message_to_all(message, WS_USERS):
    await asyncio.gather(
        *[ws.send(message) for ws in WS_USERS],
        return_exceptions=False,
    )