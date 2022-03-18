import cv2
from camutils.CamutilsModule import get_path_of_recoding
from threading import Thread
from fps.fps import FPS


class SingleVideoCamera:
    ERROR_TOLERANCE = 10

    def __init__(self, channel, resolution=(1280, 720), record=False, session_name="", show_fps=False):
        (width, height) = resolution

        self.channel = channel
        self.errors = 0
        self.stopped = False

        self.__print('is on creation')

        self.cap = cv2.VideoCapture(channel, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.resolution = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if (self.cap.isOpened() == False):
            raise Exception('Unable to read camera feed')

        self.frame = self.__getFrame()

        if resolution != self.resolution:
            self.__print('Requested resolution: ' + str(resolution) +
                         '\tGiven resolution: ' + str(self.resolution))

        if show_fps:
            self.FPS = FPS().start()

        if record == True:
            outputPath = get_path_of_recoding(session_name, channel)
            outputFormat = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

            out = cv2.VideoWriter(
                outputPath, outputFormat, 10, self.resolution)

            if (out.isOpened() == False):
                self.__print('Unable to record camera feed')

            self.out = out

    def start(self):
        Thread(target=self.__update, args=()).start()
        return self

    def getFrame(self):
        return self.frame

    def __update(self):
        while True:
            if self.stopped:
                return

            self.frame = self.__getFrame()

            if self.__isLoggingFPS() and self.FPS._numFrames % 600 == 0:
                self.FPS.stop()
                self.__print(str(self.FPS.fps()))
                self.FPS.start()
                self.FPS.update()

    def __getFrame(self):
        success, frame = self.cap.read()

        if success == True:
            if self.__isRecording():
                self.out.write(frame)

            self.errors = 0

            return frame
        else:
            self.errors += 1
            raise Exception('NO FRAME')

    def __isRecording(self):
        return hasattr(self, 'out')

    def __isLoggingFPS(self):
        return hasattr(self, 'FPS')

    def __print(self, msg):
        print('Cam: ' + str(self.channel) + '\t' + msg)

    def __del__(self):
        self.__print(' is deleted')
        self.stopped = True
        self.cap.release()
        if self.__isRecording():
            self.out.release()
