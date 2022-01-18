import cv2
from SingleVideoFeedModule import SingleVideoFeed

cam = SingleVideoFeed('recordings/recording_1641928970890_ch_0.avi')
prevFrame = None
while(True):
    frames = cam.getFrames()
    frame = frames[0]

    if frame is None:
        frame = prevFrame

    cv2.imshow('frame', frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    prevFrame = frame

cv2.destroyAllWindows()
