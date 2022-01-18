import cv2


class SingleVideoFeed:
    def __init__(self, file):
        self.cap = cv2.VideoCapture(file)
        self.file = file

        if (self.cap.isOpened() == False):
            raise Exception('Unable to read video feed')

    def getFrames(self):
        success, frame = self.cap.read()

        if success == True:
            return [frame]
        else:
            return [None]

    def __del__(self):
        self.cap.release()
