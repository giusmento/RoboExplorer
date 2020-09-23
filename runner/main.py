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
from threads.th_start_camera_service import th_start_camera_service
from library.queue.RoboQueue import RoboQueue
from library.robot.RoboExplorer import RoboExplorer
from controls.RoboControl_EasyMove import RoboControl_EasyMove

#Inizialize thread communication
roboQueue = RoboQueue()
roboQueue.create(WEBSOCKET_QUEUE)

# inizialize websocket
webSocketServer = WebSocketServer()

# create robot instance
roboExplorer = RoboExplorer()
# Start robot controller
roboControl = RoboControl_EasyMove(roboExplorer)

try:
    # START THREADS
    asyncio.get_event_loop().create_task(th_broadcast_robo_status(roboControl, roboQueue))
    asyncio.get_event_loop().create_task(th_ultrasonicsensor(roboControl, roboQueue))
    # START WEB SOCKET SERVER
    asyncio.get_event_loop().run_until_complete(webSocketServer.start(roboControl, HOST_ADDRESS, HOST_PORT))
    # START WEBSOCKET SEND SERVICE
    asyncio.get_event_loop().create_task(th_broadcast_queue(webSocketServer, roboQueue))

    # START API THREAD SERVICE
    asyncio.get_event_loop().create_task(th_start_camera_service(roboControl))
    # RUN FOREVER
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    # EXIT ON CONTROL+C
    print("Received exit, exiting")
finally:
    print("Received exit, exiting")

logger.info("goodbye")