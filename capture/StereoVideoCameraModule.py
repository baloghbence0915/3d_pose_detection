from datetime import datetime

from .SingleVideoCameraModule import SingleVideoCamera


class StereoVideoCamera:
    def __init__(self, channels, resolution=(1280, 720), record=False):
        self.__print('Init')
        now = datetime.now()
        session_name = 'camera_{0}'.format(now.strftime('%Y%m%d%H%M%S%f'))

        self.leftCam = SingleVideoCamera(
            channels[0], resolution, record, session_name).start()

        self.rightCam = SingleVideoCamera(
            channels[1], resolution, record, session_name).start()

    def getFrames(self):
        return {"left": self.leftCam.getFrame(), "right": self.rightCam.getFrame()}

    def __print(self, str):
        print('SeteroCam:\t'+str)

    def __del__(self):
        self.__print('Deleted')
        self.leftCam.stop()
        self.rightCam.stop()
        del self.leftCam
        del self.rightCam
