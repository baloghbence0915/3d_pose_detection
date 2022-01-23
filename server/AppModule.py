from capture.StereoCameraModule import StereoCamera
from capture.StereoVideoFeedModule import StereoVideoFeed
from pose.PoseDetectionModule import PoseDetection
from config.ConfigModule import Config
from calculations.CalculationsModule import getDistanceOfPoint, linearFn
from calibration.CalibrationModule import Undistortion
from camutils.CamutilsModule import rotate_image


def unwrapCoords(points, i):
    return points["left"][i]['x'], points["left"][i]['y'], points["right"][i]['x'], points["right"][i]['y']

# leftX, leftY, rightX, rightY = unwrapCoords(points, i)


class App:

    def __init__(self):
        self.cams = None
        self.detectors = None
        self.config = Config()
        self.undistortion = Undistortion()
        self.rotate_image = rotate_image

        if self.cams is None:
            self.__update_cams()

    def getFramesForPreview(self):
        frames = self.__getFrames()
        debug = self.config.get()['debug']
        show_landmarks = debug['show_landmarks']
        show_vert_hor_line = debug['show_vert_hor_line']

        if show_landmarks:
            for side, frame in frames.items():
                if frame is None:
                    continue

                (_, landmarked) = self.detectors[side].getPositions(frame)
                frames[side] = landmarked

        if show_vert_hor_line:
            for side, frame in frames.items():
                if frame is None:
                    continue
                halfHeight = int(frame.shape[0]/2)
                halfWidth = int(frame.shape[1]/2)
                frame[:, halfWidth-1:halfWidth+1] = [0, 0, 255]
                frame[halfHeight-1:halfHeight+1, :] = [0, 0, 255]

        return frames

    def getKeyPoints(self):
        frames = self.__getFrames()

        calculations = self.config.get()['calculations']
        stereo_baseline = calculations["stereo_baseline"]
        horizontal_angle = calculations["horizontal_angle"]
        stereo_scale = calculations["stereo_scale"]

        move_points_to_center = calculations["move_points_to_center"]
        offset = calculations["offset"]
        align_ground = calculations["align_ground"]
        normalize_height = calculations["normalize_height"]

        if move_points_to_center and offset['enabled']:
            raise 'Cannot move points to the center and set offset the same time!'

        resp = dict({"left": None, "right": None, "middle": {}})

        for side, frame in frames.items():
            if frame is None:
                continue

            (pose, _) = self.detectors[side].getPositions(frame)

            if pose.pose_landmarks is not None:
                resp[side] = {id: dict({'x': l.x, 'y': 1-l.y})
                              for id, l in enumerate(pose.pose_landmarks.landmark)}

        if resp['left'] is not None and resp['right'] is not None:
            # difference from X and Z axis
            diffX = 0
            diffZ = 0
            # 11 - left_shoulder ; 12 - right_shoulder
            for i in [11, 12]:
                leftX, _, rightX, _ = unwrapCoords(resp, i)
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
                leftX, leftY, rightX, rightY = unwrapCoords(resp, i)

                x = (leftX+rightX)/2
                y = (leftY+rightY)/2
                z = getDistanceOfPoint(leftX, rightX, horizontal_angle, stereo_baseline, stereo_scale)

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

                resp["middle"][i] = {'x': x, 'y': y, 'z': z}

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

        should_reset = newChannels['left'] != oldChannels['left'] or newChannels[
            'right'] != oldChannels['right'] or newShowLandmarks != oldShowLandmarks or newRecord != oldRecord or newPlay != oldPlay
        self.config.setAll(newConfig)

        if should_reset:
            self.__update_cams()

    def __getFrames(self):
        frames = self.cams.getFrames()
        mods = self.config.get()['camera']['mods']

        for side, frame in frames.items():
            if frame is None:
                continue

            if mods['all']['undistortion']:
                frame = self.undistortion.execute(frame)

            rot = mods[side]['rot']
            if rot > 0:
                frame = rotate_image(frame, rot * 90)

            frames[side] = frame

        return frames

    def __update_cams(self):
        self.cams = None

        channels = self.config.get()['camera']['channels']
        record = self.config.get()['playback']['recoding']
        play = self.config.get()['playback']['playing']['enabled']

        if play:
            file = self.config.get()['playback']['playing']['file']
            self.cams = StereoVideoFeed(
                [channels['left'], channels['right']], file)
        else:
            self.cams = StereoCamera(
                [channels['left'], channels['right']], requested_resolution=(1280, 700), record=record)

        show_landmarks = self.config.get()['debug']['show_landmarks']
        self.detectors = {"left": PoseDetection(
            show_landmarks), "right": PoseDetection(show_landmarks)}
