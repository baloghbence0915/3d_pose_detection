import cv2
from capture.StereoCameraModule import StereoCamera
from pose.PoseDetectionModule import PoseDetection
import numpy as np

video =  StereoCamera([0, 1], requested_resolution=(1280, 700), record=False)
detector1 = PoseDetection(True)
detector2 = PoseDetection(True)

while(True):
    frames = video.getFrames()

    for i, f in enumerate(frames):
        detector = detector1 if i == 0 else detector2

        pos, landmarks = detector.getPositions(f)
        
        if i == 0:
            landmarks = np.rot90(landmarks, 1)
        else:
            landmarks = np.rot90(landmarks, -1)

        cv2.imshow('landmarks' + str(i), landmarks)

    # cv2.imshow('frame 1', np.rot90(frames[0], 1))
    # cv2.imshow('frame 2', np.rot90(frames[1], -1))

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
