import numpy as np
import multiprocessing
from capture.StereoVideoCameraModule import StereoVideoCamera
from capture.StereoVideoPlayerModule import StereoVideoPlayer
from pose.PoseDetectionModule import PoseDetection
from pose.PoseLandmarksModule import drawLandmarks
from config.ConfigModule import Config
from calculations.CalculationsModule import getDistanceOfPoint, linearFn, getBodyAngle, getSpeed, unwrapCoords
from calibration.CalibrationModule import Undistortion
from camutils.CamutilsModule import rotateImage
from threading import Thread
from fps.fps import FPS


class App:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls.instance.__print('Init')
            cls.instance.config = Config()
            cls.instance.undistortion = Undistortion()
            cls.instance.frames = None
            cls.instance.poses = None
            cls.instance.stopped = False
            cls.instance.__update_cams()
            cls.instance.thread = None

        return cls.instance

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.__update, args=())
            self.thread.daemon = True
            self.thread.start()
        return self

    def __update(self):
        fps = FPS().start()
        self.__print('Start processing thread')
        while True:
            if self.stopped == True:
                break
            frames = self.cams.getFrames()
            poses = {'left': None, 'right': None}

            for side in frames.keys():
                self.__applyImageModifiers(frames, poses, side)

            self.frames = frames
            self.poses = poses

            fps.update()
            if (fps._numFrames % 60) == 0:
                fps.stop()
                self.__print('Processing FPS is: ' + str(fps.fps()))
        self.__print('Stop processing thread')

    def stop(self):
        self.stopped = True

    def getFrames(self):
        debug = self.config.get()['debug']
        show_landmarks = debug['show_landmarks']
        show_vert_hor_line = debug['show_vert_hor_line']

        frames = {"left": np.copy(
            self.frames['left']), "right": np.copy(self.frames['right'])}

        def doThing(x):
            return x*x

        if __name__ == '__main__':
            pool = multiprocessing.Pool(4)
            res = pool.map(doThing, range(0, 5))
            print(res)

        if show_landmarks or show_vert_hor_line:
            for side, frame in frames.items():
                if show_landmarks and self.poses is not None and self.poses[side] is not None:
                    drawLandmarks(frame, self.poses[side])
                if show_vert_hor_line:
                    halfHeight = int(frame.shape[0]/2)
                    halfWidth = int(frame.shape[1]/2)
                    frame[:, halfWidth-1:halfWidth+1] = [0, 0, 255]
                    frame[halfHeight-1:halfHeight+1, :] = [0, 0, 255]

        return frames

    def getKeyPoints(self):
        show_points_per_side = self.config.get(
        )['debug']['show_points_per_side']

        calculations = self.config.get()['calculations']
        stereo_baseline = calculations["stereo_baseline"]
        horizontal_angle = calculations["horizontal_angle"]
        stereo_scale = calculations["stereo_scale"]

        move_points_to_center = calculations["move_points_to_center"]
        offset = calculations["offset"]
        align_ground = calculations["align_ground"]
        normalize_height = calculations["normalize_height"]

        if move_points_to_center and offset['enabled']:
            raise Exception(
                'Cannot move points to the center and set offset the same time!')

        points = {"left": None, "right": None}
        resp = {"points": {}}
        ratio = 0

        for side, frame in self.frames.items():
            if frame is None:
                continue

            ratio = frame.shape[0] / frame.shape[1]

            pose = self.poses[side]

            if pose is not None and pose.pose_landmarks is not None:
                points[side] = {id: {'x': l.x, 'y': (
                    1-l.y)*ratio} for id, l in enumerate(pose.pose_landmarks.landmark)}

        if points['left'] is not None and points['right'] is not None:
            # difference from X and Z axis
            diffX = 0
            diffZ = 0
            # 11 - left_shoulder ; 12 - right_shoulder
            for i in [11, 12]:
                leftX, _, rightX, _ = unwrapCoords(points, i)
                diffX += (leftX + rightX)/2
                diffZ += getDistanceOfPoint(leftX, rightX,
                                            horizontal_angle, stereo_baseline, stereo_scale)
            diffX /= 2
            diffZ /= 2

            algGround = 0
            if align_ground['enabled']:
                algGround = linearFn(
                    diffZ, align_ground['slope'], align_ground['bias'])

            normHeight = 1
            if normalize_height['enabled']:
                normHeight = linearFn(
                    diffZ, normalize_height['slope'], normalize_height['bias'])

            for i in range(33):
                leftX, leftY, rightX, rightY = unwrapCoords(points, i)

                x = (leftX+rightX)/2
                y = (leftY+rightY)/2
                z = getDistanceOfPoint(
                    leftX, rightX, horizontal_angle, stereo_baseline, stereo_scale)

                #
                if align_ground['enabled']:
                    y += algGround

                #
                if move_points_to_center:
                    x -= diffX
                    z -= diffZ

                #
                if normalize_height['enabled']:
                    if not move_points_to_center:
                        x -= diffX
                        z -= diffZ
                    x *= normHeight
                    y *= normHeight
                    z *= normHeight
                    if not move_points_to_center:
                        x += diffX
                        z += diffZ

                #
                if offset['enabled']:
                    x += offset['x']
                    z += offset['z']

                resp["points"][i] = {'x': -x, 'y': y, 'z': z}

        resp['angle'] = getBodyAngle(resp['points'])
        resp['speed'] = getSpeed(resp['points'])

        resp['debug'] = {'ratio': ratio}

        if show_points_per_side:
            resp['debug']['left'] = points['left']
            resp['debug']['right'] = points['right']

        return resp

    def getConfig(self):
        return self.config.get()

    def setConfig(self, newConfig):
        newChannels = newConfig['camera']['channels']
        oldChannels = self.config.get()['camera']['channels']
        newShowLandmarks = newConfig['debug']['show_landmarks']
        oldShowLandmarks = self.config.get()['debug']['show_landmarks']
        newRecord = newConfig['playback']['recoding']
        oldRecord = self.config.get()['playback']['recoding']
        newPlay = newConfig['playback']['playing']['enabled']
        oldPlay = self.config.get()['playback']['playing']['enabled']
        newFile = newConfig['playback']['playing']['file']
        oldFile = self.config.get()['playback']['playing']['file']
        newResolution = tuple(newConfig['camera']['resolution'])
        oldResolution = tuple(self.config.get()['camera']['resolution'])

        self.config.setAll(newConfig)

        if (
            newChannels['left'] != oldChannels['left'] or
            newChannels['right'] != oldChannels['right'] or
            newShowLandmarks != oldShowLandmarks or
            newRecord != oldRecord or
            newPlay != oldPlay or
            newFile != oldFile or
            newResolution != oldResolution
        ):
            self.__update_cams()

    def __applyImageModifiers(self, frames, poses, side):
        frame = frames[side]
        mods = self.config.get()['camera']['mods']
        rot = mods[side]['rot']
        undistortion = mods['all']['undistortion']['enabled']

        if undistortion:
            frame = self.undistortion.execute(frame)

        if rot > 0:
            frame = rotateImage(frame, rot * 90)

        if side == 'left':
            poses[side] = self.detectors[side].getPose(frame)

        frames[side] = frame

    def __update_cams(self):
        self.__print("Updating cams")
        camera = self.config.get()['camera']
        channels = camera['channels']
        resolution = tuple(camera['resolution'])

        playback = self.config.get()['playback']
        record = playback['recoding']
        play = playback['playing']['enabled']
        file = playback['playing']['file']

        self.frames = {
            "left": np.zeros((resolution[0], resolution[1], 3), np.uint8),
            "right": np.zeros((resolution[0], resolution[1], 3), np.uint8),
        }

        self.poses = {'left': None, 'right': None}

        if play and file:
            self.cams = StereoVideoPlayer(
                [channels['left'], channels['right']], file)
        else:
            self.cams = StereoVideoCamera(
                [channels['left'], channels['right']], resolution=resolution, record=record)

        self.detectors = {"left": PoseDetection(), "right": PoseDetection()}
        self.__print("Updating cams done")

    def __print(self, str):
        print('App:\t'+str)

    def __del__(self):
        self.stopped = True
        del self.cams
