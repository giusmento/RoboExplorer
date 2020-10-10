import cv2
import logging
from config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(format= LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class RoboCam:

    def __init__(self, index_cam):
        self.__index_cam = index_cam
        self.__SLEEP_GET_TIME = 0.1
        self.cv = None
        self.__initialize()
        pass

    def __initialize(self):
        self.cv = cv2.VideoCapture(self.__index_cam)

    def capture_raw_frame(self):
        ret, frame = self.cv.read()
        return ret, frame

    # format: the frame format output ex. '.jpg'
    def capture_coded_frame(self, format):
        ret, frame = self.cv.read()
        if frame is not None:
            ret, coded = cv2.imencode(format, frame)
            return coded.tobytes()
        else:
            logger.error("Frame is empty")
            return None