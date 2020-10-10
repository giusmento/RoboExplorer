import subprocess
import logging
import asyncio
from controls.RoboControl import RoboControl

FORMAT = '%(asctime)s  %(name)s  %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def th_start_camera_service(roboControl:RoboControl):

    subproc = None;
    roboControl.roboExplorer.camera = True;
    while True:
        if roboControl.roboExplorer.camera:
            if subproc is None:
                logger.info('start subprocess camera service')
                command = ['python', 'cameraservice/cameraservice.py']
                subproc = subprocess.Popen(command, stdin=subprocess.PIPE)
        else:
            if subproc is not None:
                logger.info('terminating subprocess api service')
                subproc.terminate()
                subproc = None
        await asyncio.sleep(5)
