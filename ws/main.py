import logging
from ws.gpio_conf import gpio_conf
from ws.parse_args import *
from ws.config import *

logging.basicConfig(format= LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# configure GPIO
gpio_conf(MOCK_GPIO, PIGPIO_ADDR)

#Load needed gpio files
from ws.WebSocketServer import *
from ws.ws_services.ws_ultrasonicsensor import ws_ultrasonicsensor
from ws.ws_services.ws_broadcast_robo_status import ws_broadcast_robo_status
from ws.ws_services.ws_broadcast_queue import ws_broadcast_queue
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
    asyncio.get_event_loop().create_task(ws_broadcast_robo_status(roboControl))
    asyncio.get_event_loop().create_task(ws_ultrasonicsensor(roboControl, roboQueue))
    # START WEB SOCKET SERVER
    asyncio.get_event_loop().run_until_complete(webSocketServer.start(HOST_ADDRESS, HOST_PORT))
    # START WEBSOCKET SEND SERVICE
    asyncio.get_event_loop().create_task(ws_broadcast_queue(webSocketServer, roboQueue))
    # RUN FOREVER
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    # EXIT ON CONTROL+C
    print("Received exit, exiting")
finally:
    print("Received exit, exiting")

logger.info("goodbye")