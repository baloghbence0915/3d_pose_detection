import cv2
import time


class SingleCamera:
    def __init__(self, channel=0, record=False):
        self.cap = cv2.VideoCapture(channel, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 719)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.record = record
        self.channel = channel
        print(self.frame_width, self.frame_height)

        if record == True:
            self.out = cv2.VideoWriter(
                '../recordings/recording_' + str(int(time.time() * 1000)) + '_ch_' + str(channel) + '.avi',
                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                10,
                (self.frame_width, self.frame_height)
            )

            if (self.out.isOpened() == False):
                raise Exception('Unable to record camera feed')

        if (self.cap.isOpened() == False):
            raise Exception('Unable to read camera feed')

    def getFrames(self):
        success, frame = self.cap.read()

        if success == True:
            if self.record == True:
                self.out.write(frame)

            return [frame]
        else:
            raise Exception(
                'Frame cannot be requested from camera: ' + str(self.channel))

    def __del__(self):
        # self.cap.release()
        # if self.record == True:
        #     self.out.release()
        pass
