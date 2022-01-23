import cv2
from StereoCameraModule import StereoCamera
import numpy as np

cams = StereoCamera([0, 1], requested_resolution=(1280, 719), record=False)

while(True):
    frames = cams.getFrames()
    cv2.imshow('frame 1', np.rot90(frames[0], 1))
    cv2.imshow('frame 2', np.rot90(frames[1], -1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
