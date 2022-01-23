from warnings import warn

from .SingleVideoFeedModule import SingleVideoFeed
from camutils.CamutilsModule import get_path_of_recoding


class StereoVideoFeed:
    def __init__(self, channels, file):
        files = [get_path_of_recoding(
            file, channels[0]), get_path_of_recoding(file, channels[1])]
        self.files = files

        self.setUpCams()

    def getFrames(self):
        if (self.leftCam is not None and self.leftCam.done) or (self.rightCam is not None and self.rightCam.done):
            self.setUpCams()

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

    def setUpCams(self):
        self.leftCam = None
        try:
            self.leftCam = SingleVideoFeed(self.files[0])
        except Exception as e:
            warn(str(e))

        self.rightCam = None
        try:
            self.rightCam = SingleVideoFeed(self.files[1])
        except Exception as e:
            warn(str(e))
