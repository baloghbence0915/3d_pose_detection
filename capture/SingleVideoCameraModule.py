import os
import cv2
import random  
import string 
import numpy as np
from camutils.CamutilsModule import getPathOfRecoding

ERROR_TOLERANCE = 10

def getBackend():
    win = cv2.CAP_DSHOW
    lin = cv2.CAP_V4L2

    if os.name == "nt":
        return win
    else:
        return lin


class SingleVideoCamera:

    def __init__(self, channel, resolution=(1280, 720), record=False, session_name=""):
        (width, height) = resolution

        self.channel = channel
        self.errors = 0
        self.thread = None
        self.id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        self.__print('Init')

        self.cap = cv2.VideoCapture(self.channel, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.resolution = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.emptyFrame = np.zeros((width, height, 3), np.uint8) + 100

        if self.cap.isOpened() == False:
            self.__print('Unable to read camera feed')

        if resolution != self.resolution:
            self.__print('Requested resolution: ' + str(resolution) +
                         '\tGiven resolution: ' + str(self.resolution))

        if record == True:
            outputPath = getPathOfRecoding(session_name, channel)
            outputFormat = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            out = cv2.VideoWriter(
                outputPath, outputFormat, 10, self.resolution)
            if (out.isOpened() == False):
                self.__print('Unable to record camera feed')
            else:
                self.out = out
             
    def getFrame(self):
        if self.cap.isOpened():
            success, frame = self.cap.read()
            if success == True:
                if self.__isRecording():
                    self.out.write(frame)
                self.errors = 0
                return frame
        return self.emptyFrame

    def __isRecording(self):
        return hasattr(self, 'out')

    def __print(self, msg):
        print('Cam<' + self.id + ',' + str(self.channel) + '>: ' + '\t' + msg)

    def __del__(self):
        self.__print('Deleted')
        self.cap.release()
        if self.__isRecording():
            self.out.release()
