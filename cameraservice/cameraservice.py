from flask import Flask, render_template, Response
from library.camera.RoboCam import RoboCam


# GLOBAL CAM CONF
__CAM_HOST = "0.0.0.0"
__CAM_PORT = 5001

# Start application
camservice = Flask(__name__)

@camservice.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

@camservice.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(__generate_stream(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def __generate_stream():
    while True:
        #get camera frame
        jpg_frame = roboCam.capture_coded_frame('.jpg')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_frame + b'\r\n\r\n')

if __name__ == '__main__':
    roboCam = RoboCam(1)
    camservice.run(host=__CAM_HOST, port=__CAM_PORT)