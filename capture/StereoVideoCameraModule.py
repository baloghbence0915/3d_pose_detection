from datetime import datetime
from warnings import warn

from .SingleVideoCameraModule import SingleVideoCamera


class StereoVideoCamera:
    def __init__(self, channels, requested_resolution=(1280, 720), record=False, show_fps=False):
        now = datetime.now()
        session_name = 'camera_{0}'.format(now.strftime('%Y%m%d%H%M%S%f'))

        self.leftCam = None
        try:
            self.leftCam = SingleVideoCamera(
                channels[0], requested_resolution, record, session_name, show_fps).start()
        except Exception as e:
            warn(str(e))

        self.rightCam = None
        try:
            self.rightCam = SingleVideoCamera(
                channels[1], requested_resolution, record, session_name, show_fps).start()
        except Exception as e:
            warn(str(e))

    def getFrames(self):
        leftFrame = self.leftCam.getFrame()
        rightFrame = self.rightCam.getFrame()

        return dict({"left": leftFrame, "right": rightFrame})

    def getLeftFrame(self):
        return self.leftCam.getFrame()

    def getRightFrame(self):
        return self.rightCam.getFrame()

    def __del__(self):
        print('Stereo cam is deleted')
        del self.leftCam
        del self.rightCam
