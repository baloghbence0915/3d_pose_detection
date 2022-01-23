from datetime import datetime
from warnings import warn

from .SingleCameraModule import SingleCamera


class StereoCamera:
    def __init__(self, channels, requested_resolution=(1280, 720), record=False):
        now = datetime.now()
        session_name = 'camera_{0}'.format(now.strftime('%Y%m%d%H%M%S%f'))

        self.leftCam = None
        try:
            self.leftCam = SingleCamera(
                channels[0], requested_resolution, record, session_name)
        except Exception as e:
            warn(str(e))

        self.rightCam = None
        try:
            self.rightCam = SingleCamera(
                channels[1], requested_resolution, record, session_name)
        except Exception as e:
            warn(str(e))

    def getFrames(self):
        leftFrame = None
        try:
            leftFrame = self.leftCam.getFrame()
        except:
            pass

        rightFrame = None
        try:
            rightFrame = self.rightCam.getFrame()
        except:
            pass

        return dict({"left": leftFrame, "right": rightFrame})
