from warnings import warn

from .SingleVideoPlayerModule import SingleVideoPlayer
from camutils.CamutilsModule import get_path_of_recoding


class StereoVideoPlayer:
    def __init__(self, channels, file):
        self.files = [get_path_of_recoding(
            file, channels[0]), get_path_of_recoding(file, channels[1])]

        self.__setUpCams()

    def getFrames(self):
        if (self.leftCam is not None and self.leftCam.done) or (self.rightCam is not None and self.rightCam.done):
            self.__setUpCams()

        leftFrame = self.leftCam.getFrame()
        rightFrame = self.rightCam.getFrame()

        return dict({"left": leftFrame, "right": rightFrame})

    def getLeftFrame(self):
        return self.leftCam.getFrame()

    def getRightFrame(self):
        return self.rightCam.getFrame()

    def __setUpCams(self):
        self.leftCam = None
        try:
            self.leftCam = SingleVideoPlayer(self.files[0])
        except Exception as e:
            warn(str(e))

        self.rightCam = None
        try:
            self.rightCam = SingleVideoPlayer(self.files[1])
        except Exception as e:
            warn(str(e))

    def __del__(self):
        print('Stereo player is deleted')
        del self.leftCam
        del self.rightCam