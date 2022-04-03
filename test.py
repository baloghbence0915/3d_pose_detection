import cv2
import multiprocessing
import threading
import random
import string
import json
import time
from flask import Flask, render_template, Response, stream_with_context, request, after_this_request, jsonify
from flask_cors import CORS, cross_origin
from calibration.CalibrationModule import Undistortion
from camutils.CamutilsModule import applyImageModifiers, getKeyPoints

from capture.SingleVideoCameraModule import SingleVideoCamera
from config.ConfigModule import Config
from pose.PoseDetectionModule import PoseDetection
from pose.PoseLandmarksModule import drawLandmarks
from fps.fps import FPS


def rec(getCap, pipe):
    cap, det, side = getCap()
    frame = None
    fps = FPS(100, cap.id).start()
    config = Config()
    undistortion = Undistortion()
    while True:
        f = cap.getFrame()
        (frame, pose) = applyImageModifiers(f, side, config, det, undistortion)
        fps.update()
        pipe.send((frame, pose))


def getLeftCap():
    cap1 = SingleVideoCamera(0, (640, 480))
    det1 = PoseDetection()

    return (cap1, det1, 'left')


def getRightCap():
    cap2 = SingleVideoCamera(1, (640, 480))
    det2 = PoseDetection()

    return (cap2, det2, 'right')


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    pipeLeftBegin, pipeLeftEnd = multiprocessing.Pipe(duplex=True)
    pipeRightBegin, pipeRightEnd = multiprocessing.Pipe(duplex=True)

    proc1 = multiprocessing.Process(
        target=rec, args=[getLeftCap, pipeLeftBegin], daemon=True)
    proc2 = multiprocessing.Process(
        target=rec, args=[getRightCap, pipeRightBegin], daemon=True)
    proc1.start()
    proc2.start()

    frameLeft = None
    frameRight = None
    poseLeft = None
    poseRight = None

    def run():
        global frameLeft, frameRight, poseLeft, poseRight
        show = True
        while True:
            if not proc1.is_alive() and not proc2.is_alive():
                break

            (frameLeft, poseLeft) = pipeLeftEnd.recv()
            (frameRight, poseRight) = pipeRightEnd.recv()

            drawLandmarks(frameLeft, poseLeft)
            drawLandmarks(frameRight, poseRight)

            if show:
                cv2.imshow('left', frameLeft)
                cv2.imshow('right', frameRight)

            if cv2.waitKey(1) == ord('q'):
                # proc1.kill()
                # proc2.kill()
                # break
                show = False
                cv2.destroyAllWindows()


    threading.Thread(target=run, daemon=True).start()
    print('Leave pool')

    host = "0.0.0.0"
    port = 8080
    flask = Flask(__name__)
    cors = CORS(flask)

    @flask.route('/api')
    @cross_origin()
    def health_check():
        return 'done', 200

    # @flask.route('/api/config', methods=['GET', 'POST'])
    # @cross_origin()
    # def config():
    #     if request.method == 'GET':
    #         return jsonify(app.getConfig())
    #     elif request.method == 'POST':
    #         config = request.json
    #         if config is None:
    #             return 'Mime type is not json or body is empty', 400
    #         app.setConfig(config)
    #         return jsonify(app.getConfig())

    # @flask.route('/api/recordings')
    # @cross_origin()
    # def recordings():
    #     return jsonify(getRecordings())

    config = Config()

    @flask.route('/api/stream/frame/<side>', methods=['GET'])
    @cross_origin()
    def stream_frame(side):
        def genFrames():
            while True:
                time.sleep(0.01)
                frame = frameLeft if side == 'left' else frameRight
                if frame is None:
                    return
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @flask.route('/api/stream/keypoints')
    @cross_origin()
    def stream_keypoints():
        def genKeypoints():
            while True:
                time.sleep(0.05)
                keyPoints = getKeyPoints(
                    {'left': frameLeft, 'right': frameRight}, {'left': poseLeft, 'right': poseRight}, config)
                yield ('data:' + json.dumps(keyPoints) + '\n\n')

        return Response(genKeypoints(), mimetype='text/event-stream')

    @flask.route('/')
    def index():
        return render_template('index.html')

    flask.run(debug=False, host=host, port=port)
