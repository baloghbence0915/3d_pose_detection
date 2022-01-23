import io
import cv2
import bson
import json
from PIL import Image

from server.AppModule import App
from server.RouterModule import Router
from camutils.CamutilsModule import get_recordings

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

class APIServer(Router):
    app = App()

    def GET_api_frame(self):
        self.send_header("Content-type", "multipart/x-mixed-replace; boundary=frame")
        self.end_headers()
        self.wfile.write(next(gen_frames()))

    def GET_api_frames(self):
        self.send_header("Content-type", "application/bson")
        self.end_headers()

        frames = APIServer.app.getFramesForPreview()
        response = dict({})

        for side, frame in frames.items():
            response[side] = {"frame": None, "res": [0, 0]}

            if frame is None:
                continue

            h, w, _ = frame.shape

            with io.BytesIO() as output:
                im = Image.fromarray(cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB), 'RGB')
                im.save(output, format='JPEG')
                frame = output.getvalue()

            response[side] = {"frame": frame, "res": [h, w]}

        self.wfile.write(bson.dumps(response))

    def GET_api_points(self):
        self.send_header("Content-type", "application/json")
        self.end_headers()

        points = self.app.getKeyPoints()

        self.wfile.write(bytes(json.dumps(points), 'utf-8'))

    def GET_api_config(self):
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(self.app.getConfig()), 'utf-8'))

    def POST_api_config(self):
        length = int(self.headers.get('content-length'))
        newConfig = json.loads(self.rfile.read(length))
        self.app.setConfig(newConfig)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(
            bytes(json.dumps(self.app.getConfig()), 'utf-8'))

    def GET_api_recordings(self):
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(get_recordings()), 'utf-8'))

    def GET_api(self):
        self.end_headers()

