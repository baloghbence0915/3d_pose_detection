import cv2


class SingleVideoFeed:
    def __init__(self, file):
        self.cap = cv2.VideoCapture(file)
        self.file = file
        self.done = False

        if (self.cap.isOpened() == False):
            raise Exception('Unable to read video feed')

    def getFrame(self):
        success, frame = self.cap.read()

        if success == True:
            return frame
        else:
            self.done = True

    def __del__(self):
        self.cap.release()
