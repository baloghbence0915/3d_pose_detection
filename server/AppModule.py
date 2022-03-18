import math

from cv2 import undistort

from capture.StereoVideoCameraModule import StereoVideoCamera
from capture.StereoVideoPlayerModule import StereoVideoPlayer
from pose.PoseDetectionModule import PoseDetection
from config.ConfigModule import Config
from calculations.CalculationsModule import getDistanceOfPoint, linearFn, get_body_angle, get_speed
from calibration.CalibrationModule import Undistortion
from camutils.CamutilsModule import rotate_image

# leftX, leftY, rightX, rightY = unwrapCoords(points, i)


def unwrapCoords(points, i):
    return points["left"][i]['x'], points["left"][i]['y'], points["right"][i]['x'], points["right"][i]['y']


class App:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls.instance.config = Config()
            cls.instance.undistortion_module = Undistortion()
            cls.instance.rotate_image_module = rotate_image
            # cls.instance.leftFrame = None
            # cls.instance.rightFrame = None
            cls.instance.__update_cams()

        return cls.instance

    def getLeftFrameProp(self):
        return self.leftFrame

    def getRightFrameProp(self):
        return self.rightFrame

    # def __updateLeftFrame(self):
    #     while True:
    #         self.leftFrame = self.getLeftFrame()

    # def __updateLeftFrame(self):
    #     while True:
    #         self.leftFrame = self.getLeftFrame()

    def getFrames(self):
        debug = self.config.get()['debug']
        show_landmarks = debug['show_landmarks']
        show_vert_hor_line = debug['show_vert_hor_line']
        return self.__getFrames(show_landmarks, show_vert_hor_line)

    def getLeftFrame(self):
        debug = self.config.get()['debug']
        show_landmarks = debug['show_landmarks']
        show_vert_hor_line = debug['show_vert_hor_line']
        return self.__getLeftFrame(show_landmarks, show_vert_hor_line)

    def getRightFrame(self):
        debug = self.config.get()['debug']
        show_landmarks = debug['show_landmarks']
        show_vert_hor_line = debug['show_vert_hor_line']
        return self.__getRightFrame(show_landmarks, show_vert_hor_line)

    def getKeyPoints(self):
        frames = self.__getFrames(False, False)

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

        points = dict({"left": None, "right": None})
        resp = dict({"points": {}})
        ratio = 0

        for side, frame in frames.items():
            if frame is None:
                continue

            ratio = frame.shape[0] / frame.shape[1]

            (pose, _) = self.detectors[side].getPositions(frame)

            if pose.pose_landmarks is not None:
                points[side] = {id: dict({'x': l.x, 'y': (1-l.y)*ratio})
                                for id, l in enumerate(pose.pose_landmarks.landmark)}

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

        resp['angle'] = get_body_angle(resp['points'])
        resp['speed'] = get_speed(resp['points'])

        resp['debug'] = dict({'ratio': ratio})

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

    def __getFrames(self, show_landmarks, show_vert_hor_line):
        frames = self.cams.getFrames()
        mods = self.config.get()['camera']['mods']
        undistortion = mods['all']['undistortion']
        for side, frame in frames.items():
            frames[side] = self.__applyImageModifiers(
                frame, side, mods[side]['rot'], undistortion, show_landmarks, show_vert_hor_line)
        return frames

    def __getLeftFrame(self, show_landmarks, show_vert_hor_line):
        frame = self.cams.getLeftFrame()
        mods = self.config.get()['camera']['mods']
        rot = mods['left']['rot']
        undistortion = mods['all']['undistortion']
        return self.__applyImageModifiers(frame, 'left', rot, undistortion, show_landmarks, show_vert_hor_line)

    def __getRightFrame(self, show_landmarks, show_vert_hor_line):
        frame = self.cams.getRightFrame()
        mods = self.config.get()['camera']['mods']
        rot = mods['right']['rot']
        undistortion = mods['all']['undistortion']
        return self.__applyImageModifiers(frame, 'right', rot, undistortion, show_landmarks, show_vert_hor_line)

    def __applyImageModifiers(self, frame, side, rot, undistortion, show_landmarks, show_vert_hor_line):
        if frame is None:
            return

        if undistortion:
            frame = self.undistortion_module.execute(frame)

        if rot > 0:
            frame = rotate_image(frame, rot * 90)

        if show_landmarks:
            (_, landmarked) = self.detectors[side].getPositions(frame)
            frame = landmarked

        if show_vert_hor_line:
            halfHeight = int(frame.shape[0]/2)
            halfWidth = int(frame.shape[1]/2)
            frame[:, halfWidth-1:halfWidth+1] = [0, 0, 255]
            frame[halfHeight-1:halfHeight+1, :] = [0, 0, 255]

        return frame

    def __update_cams(self):
        channels = self.config.get()['camera']['channels']
        resolution = tuple(self.config.get()['camera']['resolution'])
        record = self.config.get()['playback']['recoding']
        play = self.config.get()['playback']['playing']['enabled']
        show_landmarks = self.config.get()['debug']['show_landmarks']

        if play:
            file = self.config.get()['playback']['playing']['file']
            self.cams = StereoVideoPlayer(
                [channels['left'], channels['right']], file)
        else:
            self.cams = StereoVideoCamera(
                [channels['left'], channels['right']], requested_resolution=resolution, record=record)

        self.detectors = {"left": PoseDetection(
            show_landmarks), "right": PoseDetection(show_landmarks)}
