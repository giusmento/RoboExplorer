import cv2
from cv2 import *
import subprocess as sp

if __name__ == "__main__":
    rtsp_server = 'udp://224.3.29.71:10000'  # push server (output server)

    # pull rtsp data, or your cv cap.  (input server)
    cap = cv2.VideoCapture(1)
    #cap = cv2.VideoCapture("sample.mp4")

    sizeStr = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + \
              'x' + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    command = ['ffmpeg',
               ##'-re',
               '-s', sizeStr,
               '-r', str(fps),  # rtsp fps (from input server)
               '-i', '-',

               # You can change ffmpeg parameter after this item.
               # used: yuv420p, rgb24
               '-pix_fmt', 'yuv420p',
               '-r', '10',  # output fps
               '-g', '50',
               # use: libx264, libx265, libxvid, mpeg4
               '-c:v', 'mpeg4',
               '-c:a', 'mp3',
               #'-b:v', '1M',
               #'-bufsize', '64M',
               #'-maxrate', "4M",
               #'-preset', 'veryfast',

               #RTSP
               #'-rtsp_transport', 'tcp',
               #'-segment_times', '5',
               #'-f', 'rtsp',

               #RTP
               #'-ttl', '1',
               #'-f', 'rtp',

               #MPEGTS
               '-f', 'mpegts',
               #RTSP
               rtsp_server]

    process = sp.Popen(command, stdin=sp.PIPE)
    try:
        while cap.isOpened():
            ret, frame = cap.read()

            dsize = (500, 250)
            output = cv2.resize(frame, dsize)
            #cv2.imshow("client", frame)
            ret2, frame2 = cv2.imencode('.png', frame)
            process.stdin.write(frame2.tobytes())
            if cv2.waitKey(1) & 0xFF == ord("q"):  # wait until key was pressed once and
                break
        cap.release()
        cv2.destroyAllWindows()
    finally:
        print(sys.stderr, 'closing socket')