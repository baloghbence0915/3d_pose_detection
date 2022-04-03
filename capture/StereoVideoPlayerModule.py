from warnings import warn

from .SingleVideoPlayerModule import SingleVideoPlayer
from camutils.CamutilsModule import getPathOfRecoding
import time


class StereoVideoPlayer:
    def __init__(self, channels, file):
        print('Stereo player is on creation')
        self.files = [getPathOfRecoding(
            file, channels[0]), getPathOfRecoding(file, channels[1])]

        self.leftCam = SingleVideoPlayer(self.files[0])
        self.rightCam = SingleVideoPlayer(self.files[1])

    def getFrames(self):
        if self.leftCam.done or self.rightCam.done:
            self.leftCam.restart()
            self.rightCam.restart()

        return {"left": self.leftCam.getFrame(), "right": self.rightCam.getFrame()}

    def __del__(self):
        print('Stereo player is on delete')
        del self.leftCam
        del self.rightCam
