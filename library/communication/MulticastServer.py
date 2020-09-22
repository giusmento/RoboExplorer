import socket
import struct
import sys
import time
import ffmpeg
import os
import cv2
import _pickle
from cv2 import *
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

message = b'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket - MULTICAST - UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# TCP
#sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind(('localhost',8088))

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
#sock.settimeout(0.2)

cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture("sample.mp4")
#cv2.CV_FOURCC('H','2','6','4')
#fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
#cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#out = cv2.VideoWriter()
#succes = out.open('output.mp4v',fourcc, 15.0, (1280,720),True)

try:
    while cap.isOpened():
        #ret, frame = cap.read()  # reads each frame from webcam
        #cv2.imshow("client", frame)
        #out.write(frame)
        #message = _pickle.dumps(frame)
        # split message is n package of 64K
        size = sys.getsizeof(message)/65.535
        #info = [frame[i:i + 2] for i in range(0, 4200)]

        stream = ffmpeg.input('sample.mov')
        stream = ffmpeg.output(stream, 'udp://224.3.29.71:10000', f='mpegts', vcodec="copy")
        ffmpeg.run(stream)

        # for pack in info:
        #     sock.sendto(pack, multicast_group)


        if cv2.waitKey(1) & 0xFF == ord("q"):  # wait until key was pressed once and
            break
    cap.release()
    cv2.destroyAllWindows()

        # print( " sample.mov:" + str(os.path.exists("sample.mp4")))

        # # stream = ffmpeg.filter_(stream, 'drawtext', fontfile="fonts/hack/Hack-Regular.ttf", text="%{pts}", box='1',
        # #                         boxcolor='0x00000000@1', fontcolor='white')
        # stream = ffmpeg.output(stream, 'udp://224.3.29.71:10000', f='mpegts', vcodec="copy")
        # ffmpeg.run(stream)
        #
        # time.sleep(30)

    # Send data to the multicast group
    print ('sending "%s"' % message)
    sent = sock.sendto(message, multicast_group)

    # # Look for responses from all recipients
    # while True:
    #     print ('waiting to receive')
    #     sock.sendto(b"message", multicast_group)
    #     # try:
    #     #     # data, server = sock.recvfrom(16)
    #     # except socket.timeout:
    #     #     print ('timed out, no more responses')
    #     #     break
    #     # else:
    #     #     print ('received "%s" from %s' % (data, server))
    #     time.sleep(1)

finally:
    print (sys.stderr, 'closing socket')
    sock.close()