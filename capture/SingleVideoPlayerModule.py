import cv2
import numpy as np


class SingleVideoPlayer:
    def __init__(self, file, resolution=(1280, 720)):
        print('Video player is on creation:\t' + file)
        self.file = file
        self.done = False
        self.resolution = resolution
    
    def start(self):
        self.cap = cv2.VideoCapture(self.file)
        self.isOpened = self.cap.isOpened()

        if self.isOpened == False:
            print('Unable to read video feed:\t' + self.file)

        return self

    def getFrame(self):
        if self.isOpened:
            success, frame = self.cap.read()

            if success == True:
                return frame

        self.done = True
        return np.zeros((self.resolution[0], self.resolution[1], 3), np.uint8)

    def restart(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(self.file)
        self.done = False

    def __del__(self):
        print('Video player is deleted:\t' + self.file)
        self.cap.release()
