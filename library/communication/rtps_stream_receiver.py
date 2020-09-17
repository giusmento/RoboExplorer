import cv2
from cv2 import *

cap = cv2.VideoCapture('udp://224.3.29.71:10000')
#cap = cv2.VideoCapture(1)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow("client", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):  # wait until key was pressed once and
            break
    cap.release()
    cv2.destroyAllWindows()
finally:
    print(sys.stderr, 'closing socket')