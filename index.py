from flask import Flask, render_template, Response
import cv2
import threading
from controller import control

app = Flask(__name__)

camera = cv2.VideoCapture(-1)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
suc, frame = camera.read()

def gen_frame():
    while True:
        suc, frame = camera.read()
        frame = cv2.resize(frame, (0,0), fx=0.3, fy=0.3)
        if not suc:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

thread_controller = threading.Thread(target=control)
thread_controller.start()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
