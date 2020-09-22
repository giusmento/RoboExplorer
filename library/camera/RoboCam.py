import cv2
import time

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
        ret, coded = cv2.imencode(format, frame)
        return coded.tobytes()