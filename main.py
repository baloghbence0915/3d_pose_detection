import cv2
import multiprocessing
import threading
import random
import string
import json
import time
from datetime import datetime
from flask import Flask, render_template, Response, stream_with_context, request, after_this_request, jsonify
from flask_cors import CORS, cross_origin
from calibration.CalibrationModule import Undistortion
from camutils.CamutilsModule import applyImageModifiers, getKeyPoints, getRecordings

from capture.SingleVideoCameraModule import SingleVideoCamera
from capture.StereoVideoPlayerModule import StereoVideoPlayer
from config.ConfigModule import Config
from pose.PoseDetectionModule import PoseDetection
from pose.PoseLandmarksModule import drawLandmarks
from fps.fps import FPS


def captureCamera(getCap, pipe, session):
    cap, det, side = getCap(session)
    frame = None
    fps = FPS(100, cap.id).start()
    config = Config()
    undistortion = Undistortion()
    while True:
        f = cap.getFrame()
        (frame, pose) = applyImageModifiers(f, side, config, det, undistortion)
        fps.update()
        pipe.send((frame, pose))

def getCameraConfig(side):
    config = Config().get()
    camera = config["camera"]
    resolution = camera["resolution"]
    channels = camera["channels"]
    return (channels[side], resolution[0], resolution[1])


def getLeftCamera(session):
    channel, width, height = getCameraConfig('left')
    cap = SingleVideoCamera(channel, (width, height), session)
    det = PoseDetection()
    return (cap, det, 'left')


def getRightCamera(session):
    channel, width, height = getCameraConfig('right')
    cap = SingleVideoCamera(channel, (width, height), session)
    det = PoseDetection()
    return (cap, det, 'right')

def capturePlayer(getPlayer, pipeLeft, pipeRight):
    player, detLeft, detRight = getPlayer()
    frame = None
    fps = FPS(100, 'Video player').start()
    config = Config()
    undistortion = Undistortion()
    while True:
        print('read')
        frames = player.getFrames()
        for side, frame in frames.items():
            if side=='left':
                (frame, pose) = applyImageModifiers(frame, side, config, detLeft, undistortion)
                pipeLeft.send((frame, pose))
            else:
                (frame, pose) = applyImageModifiers(frame, side, config, detRight, undistortion)
                pipeRight.send((frame, pose))
        fps.update()

def getVideoPlayer():
    config = Config().get()
    camera = config["camera"]
    resolution = camera["resolution"]
    channels = camera["channels"]
    cap = StereoVideoPlayer(
        [channels['left'], channels['right']], config["playback"]["playing"]["file"], resolution)
    det1 = PoseDetection()
    det2 = PoseDetection()
    return (cap, det1, det2)

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    pipeLeftBegin, pipeLeftEnd = multiprocessing.Pipe()
    pipeRightBegin, pipeRightEnd = multiprocessing.Pipe()

    processLeft = None
    processRight = None
    processPlayer = None

    frameLeft = None
    frameRight = None
    poseLeft = None
    poseRight = None

    def startProcesses():
        global processLeft, processRight
        config = Config().get()

        if config["playback"]["playing"]["enabled"]:
            processPlayer = multiprocessing.Process(
                target=capturePlayer, args=[getVideoPlayer, pipeLeftBegin, pipeRightBegin], daemon=True)
            processPlayer.start()
        else:
            now = datetime.now()
            session = 'camera_{0}'.format(now.strftime('%Y%m%d%H%M%S%f'))

            processLeft = multiprocessing.Process(
                target=captureCamera, args=[getLeftCamera, pipeLeftBegin, session], daemon=True)
            processRight = multiprocessing.Process(
                target=captureCamera, args=[getRightCamera, pipeRightBegin, session], daemon=True)
            processLeft.start()
            processRight.start()

    def stopProcesses():
        global processLeft, processRight, processPlayer
        processes = [processLeft, processRight, processPlayer]
        for process in processes:
            if process is not None:
                process.terminate()
            process = None

    def run():
        global frameLeft, frameRight, poseLeft, poseRight, processLeft, processRight, processPlayer
        print("Main thread started")
        config = Config().get()
        isPlayback = config["playback"]["playing"]["enabled"]

        show = True
        while True:
            if isPlayback:
                if not processPlayer.is_alive():
                    break
            else:
                if not processLeft.is_alive() and not processRight.is_alive():
                    break

            if pipeLeftEnd.poll():
                (frameLeft, poseLeft) = pipeLeftEnd.recv()
            else:
                continue
            if pipeRightEnd.poll():
                (frameRight, poseRight) = pipeRightEnd.recv()
            else:
                continue
                
            if frameLeft is None or frameRight is None:
                continue

            drawLandmarks(frameLeft, poseLeft)
            drawLandmarks(frameRight, poseRight)

            if show:
                cv2.imshow('left', frameLeft)
                cv2.imshow('right', frameRight)

            if cv2.waitKey(1) == ord('q'):
                show = False
                cv2.destroyAllWindows()
        print("Main thread stopped")

    def startMainThread():
        threading.Thread(target=run, daemon=True).start()

    startProcesses()
    startMainThread()

    host = "0.0.0.0"
    port = 8080
    flask = Flask(__name__)
    cors = CORS(flask)

    @flask.route('/api')
    @cross_origin()
    def health_check():
        return 'done', 200

    @flask.route('/api/config', methods=['GET', 'POST'])
    @cross_origin()
    def config_method():
        config = Config()
        if request.method == 'GET':
            return jsonify(config.get())
        elif request.method == 'POST':
            newConfig = request.json
            if config is None:
                return 'Mime type is not json or body is empty', 400
            config.set(newConfig)
            return jsonify(config.get())

    @flask.route('/api/recordings')
    @cross_origin()
    def recordings():
        return jsonify(getRecordings())

    @flask.route('/api/restart')
    @cross_origin()
    def restart():
        stopProcesses()
        startProcesses()
        startMainThread()
        return 'restarted', 200

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
        config = Config()

        def genKeypoints():
            while True:
                time.sleep(0.05)
                keyPoints = getKeyPoints(
                    {'left': frameLeft, 'right': frameRight}, {'left': poseLeft, 'right': poseRight}, config)
                yield ('data:' + json.dumps(keyPoints) + '\n\n')

        return Response(genKeypoints(), mimetype='text/event-stream')

    # @flask.route('/')
    # def index():
    #     return render_template('index.html')

    flask.run(debug=False, host=host, port=port)
