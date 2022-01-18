from SingleCameraModule import SingleCamera


class StereoCamera:
    def __init__(self, channels=[0, 1], record=False):
        self.channels = channels,
        self.record = record
        self.cameras = [SingleCamera(channels[0],record), SingleCamera(channels[1],record), ]

    def getFrames(self):
        return [self.cameras[0].getFrames()[0], self.cameras[1].getFrames()[0]]
