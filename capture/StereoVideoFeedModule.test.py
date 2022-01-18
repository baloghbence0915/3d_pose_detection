import cv2
from StereoVideoFeedModule import StereoVideoFeed

cams = StereoVideoFeed(['recordings/recording_1641929909858_ch_0.avi',
                       'recordings/recording_1641929909928_ch_1.avi'])

prevFrames = [None, None]

while(True):
    frame0, frame1 = cams.getFrames()

    if frame0 is None or frame1 is None:
        frame0 = prevFrames[0]
        frame1 = prevFrames[1]

    cv2.imshow('frame 1', frame0)
    cv2.imshow('frame 2', frame1)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    prevFrames = [frame0, frame1]

cv2.destroyAllWindows()
