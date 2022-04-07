import cv2
import numpy as np
import random  
import string 

class SingleVideoPlayer:
    def __init__(self, file, resolution=(1280, 720)):
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.file = file
        self.__print('Video player is on creation')
        self.done = False
        self.resolution = resolution
        self.cap = cv2.VideoCapture(self.file)
        self.isOpened = self.cap.isOpened()

        if self.isOpened == False:
            self.__print('Unable to read video feed:\t' + self.file)
    
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
        self.__print('Video player is deleted:\t' + self.file)
        self.cap.release()
    
    def __print(self, msg):
        print('Player<' + self.id + ',' + str(self.file) + '>: ' + '\t' + msg)
