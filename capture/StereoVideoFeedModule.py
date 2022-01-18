from SingleVideoFeedModule import SingleVideoFeed


class StereoVideoFeed:
    def __init__(self, files):
        self.files = files,
        self.captures = [SingleVideoFeed(
            files[0]), SingleVideoFeed(files[1]), ]

    def getFrames(self):
        return [self.captures[0].getFrames()[0], self.captures[1].getFrames()[0]]
