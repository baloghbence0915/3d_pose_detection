import cv2
from SingleVideoFeedModule import SingleVideoFeed
from os.path import join

cam = SingleVideoFeed(join('..', 'recordings', 'recording_1642535760245_ch_1.avi'))
prevFrame = None
while(True):
    frame = cam.getFrame()

    if frame is None:
        frame = prevFrame

    cv2.imshow('frame', frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    prevFrame = frame

cv2.destroyAllWindows()
