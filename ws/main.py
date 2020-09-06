import asyncio
from ws.gpio_conf import gpio_conf
from ws.config import *
import logging
from ws.parse_args import *
import queue

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gpio_conf(MOCK_GPIO, PIGPIO_ADDR)

#Load needed gpio files
from ws.WebSocketServer import *
from ws.ws_services.ws_ultrasonicsensor import ws_ultrasonicsensor
from ws.ws_services.ws_broadcast_report import ws_broadcast_report
from ws.ws_services.ws_broadcast_queue import ws_broadcast_queue
from ws.ws_services.ws_robot_control import ws_robot_control
from library.robot.RoboExplorer import RoboExplorer
from controls.RoboControl_EasyMove import RoboControl_EasyMove


ws_queue = queue.Queue()

# Start robot control
roboControl = RoboControl_EasyMove()
webSocketServer = WebSocketServer()
#start_ws_server1 = webSocketServer.start(HOST_ADDRESS, HOST_PORT)

#robotExplorer = RobotExplorer(ultrasonicSensorObserver)
# START BROADCAST
logger.info("start web socket at " + HOST_ADDRESS + ":" + str(HOST_PORT))
try:
    #asyncio.get_event_loop().create_task(ws_broadcast_report())
    asyncio.get_event_loop().create_task(ws_broadcast_queue(ws_queue, webSocketServer))
    asyncio.get_event_loop().create_task(ws_ultrasonicsensor(roboControl, webSocketServer))
    #asyncio.get_event_loop().create_task(ws_robot_control())
    # START SERVER
    asyncio.get_event_loop().run_until_complete(webSocketServer.start(HOST_ADDRESS, HOST_PORT))
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("Received exit, exiting")
finally:
    #robotExplorer.close()
    print("Received exit, exiting")
logger.info("end of asyncio")