import asyncio
from ws.gpio_conf import gpio_conf
from ws.config import *
import logging
from ws.parse_args import *

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gpio_conf(MOCK_GPIO, PIGPIO_ADDR)

#Load needed gpio files
from ws.WebSocketServer import *
from ws.ws_services.ws_ultrasonicsensor import ws_ultrasonicsensor
from ws.ws_services.ws_broadcast_report import ws_broadcast_report
from ws.ws_services.ws_robot_control import ws_robot_control
from library.robot.RobotExplorer import robotExplorer

# START BROADCAST
logger.info("start web socket at " + HOST_ADDRESS + ":" + str(HOST_PORT))
try:
    asyncio.get_event_loop().create_task(ws_broadcast_report())
    asyncio.get_event_loop().create_task(ws_ultrasonicsensor())
    asyncio.get_event_loop().create_task(ws_robot_control())
    # START SERVER
    asyncio.get_event_loop().run_until_complete(start_ws_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("Received exit, exiting")
finally:
    robotExplorer.close()
    print("Received exit, exiting")
logger.info("end of asyncio")