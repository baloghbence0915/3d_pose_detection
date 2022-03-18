from flask import Flask, render_template, Response, stream_with_context, request
import cv2
# from .capture.StereoCameraModule import StereoCamera
from capture.SingleCameraModule import SingleCamera

app = Flask(__name__)

camLeft = cv2.VideoCapture(1)
camRight = cv2.VideoCapture(1)

def gen_frames(cam: cv2.VideoCapture):  # generate frame by frame from camera
    while True:
        (s, frame) = cam.read()  # read the camera frame
        if not s:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed/<side>')
def video_feed(side):
    if side == 'left':
        return Response(gen_frames(camLeft), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(gen_frames(camRight), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/stream')
# def streamed_response():
#     def generate():
#         # yield 'Hello '
#         # yield request.args['name']
#         # yield '!'
#         i = 0
#         while i < 300000000:
#             i += 1
#             if i % 10000 == 0:
#                 yield str(i) + ',' 
#     return app.response_class(stream_with_context(generate()))

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

app.run(debug=True, host='0.0.0.0', port=5000)