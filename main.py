import cv2
import sys
import json
import time
import signal
import base64
from flask import Flask, render_template, Response, stream_with_context, request, after_this_request, jsonify
from flask_cors import CORS, cross_origin
from server.AppModule import App
from fps.fps import FPS
from camutils.CamutilsModule import getRecordings

host = "0.0.0.0"
port = 8080

flask = Flask(__name__)
cors = CORS(flask)
flask.config['CORS_HEADERS'] = 'Content-Type'

app = App().start()
fps = FPS()

# def signal_handler(sig, frame):
#     print('You pressed Ctrl+C!')
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)


@flask.route('/api')
@cross_origin()
def health_check():
    return '', 200


@flask.route('/api/config', methods=['GET', 'POST'])
@cross_origin()
def config():
    if request.method == 'GET':
        return jsonify(app.getConfig())
    elif request.method == 'POST':
        config = request.json
        if config is None:
            return 'Mime type is not json or body is empty', 400
        app.setConfig(config)
        return jsonify(app.getConfig())

@flask.route('/api/recordings')
@cross_origin()
def recordings():
    return jsonify(getRecordings())


@flask.route('/api/stream/frame/<side>', methods=['GET'])
@cross_origin()
def stream_frame(side):
    def genFrames(side2):
        while True:
            frame = app.getFrames()[side2]
            if frame is None:
                return
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(genFrames(side), mimetype='multipart/x-mixed-replace; boundary=frame')


@flask.route('/api/stream/keypoints')
@cross_origin()
def stream_keypoints():
    def genKeypoints():
        while True:
            time.sleep(0.05)
            keyPoints = app.getKeyPoints()
            yield ('data:' + json.dumps(keyPoints) + '\n\n')

    return Response(genKeypoints(), mimetype='text/event-stream')
    # return jsonify(app.getKeyPoints())

@flask.route('/')
def index():
    return render_template('index.html')

flask.run(debug=False, host=host, port=port)
