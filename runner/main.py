import asyncio
import logging
from utils.gpio_conf import gpio_conf
from utils.parse_args import *
from config import *

logging.basicConfig(format= LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# configure GPIO
gpio_conf(MOCK_GPIO, PIGPIO_ADDR)

#Load needed gpio files
from library.communication.WebSocketServer import WebSocketServer
from threads.th_ultrasonicsensor import th_ultrasonicsensor
from threads.th_broadcast_robo_status import th_broadcast_robo_status
from threads.th_broadcast_queue import th_broadcast_queue
from library.queue.RoboQueue import RoboQueue
from controls.RoboControl_EasyMove import RoboControl_EasyMove

#Inizialize thread communication
roboQueue = RoboQueue()
roboQueue.create(WEBSOCKET_QUEUE)
# inizialize websocket
webSocketServer = WebSocketServer()

# Start robot control
roboControl = RoboControl_EasyMove()

try:
    # START THREADS
    asyncio.get_event_loop().create_task(th_broadcast_robo_status(roboControl))
    asyncio.get_event_loop().create_task(th_ultrasonicsensor(roboControl, roboQueue))
    # START WEB SOCKET SERVER
    asyncio.get_event_loop().run_until_complete(webSocketServer.start(HOST_ADDRESS, HOST_PORT))
    # START WEBSOCKET SEND SERVICE
    asyncio.get_event_loop().create_task(th_broadcast_queue(webSocketServer, roboQueue))
    # RUN FOREVER
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    # EXIT ON CONTROL+C
    print("Received exit, exiting")
finally:
    print("Received exit, exiting")

logger.info("goodbye")