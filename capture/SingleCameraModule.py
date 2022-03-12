import cv2
from warnings import warn
from camutils.CamutilsModule import get_path_of_recoding


class SingleCamera:
    ERROR_TOLERANCE = 10

    def __init__(self, channel, requested_resolution=(1280, 720), record=False, session_name=""):
        cap = cv2.VideoCapture(channel, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, requested_resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, requested_resolution[1])
        given_resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.cap = cap
        self.channel = channel
        self.errors = 0

        if (cap.isOpened() == False):
            raise Exception('Unable to read camera feed')

        if requested_resolution != given_resolution:
            print('Requested resolution: ' + str(requested_resolution) +
                  '\nGiven resolution: ' + str(given_resolution))

        if record == True:
            outputPath = get_path_of_recoding(session_name, channel)
            outputFormat = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

            out = cv2.VideoWriter(
                outputPath, outputFormat, 8, given_resolution)

            if (out.isOpened() == False):
                warn('Unable to record camera feed')

            self.out = out

    def getFrame(self):
        success, frame = self.cap.read()

        if success == True:
            if self.__isRecording():
                self.out.write(frame)

            self.errors = 0

            return frame

        elif self.errors >= SingleCamera.ERROR_TOLERANCE:
            raise Exception(
                'Frame cannot be requested from camera: ' + str(self.channel))

        else:
            self.errors += 1

    def __isRecording(self):
        return hasattr(self, 'out')

    def __del__(self):
        self.cap.release()
        if self.__isRecording():
            self.out.release()
