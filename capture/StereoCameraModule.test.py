import cv2
from StereoCameraModule import StereoCamera

cams = StereoCamera([1,2], record=False)

while(True):
    frames = cams.getFrames()
    cv2.imshow('frame 1', frames[0])
    cv2.imshow('frame 2', frames[1])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
