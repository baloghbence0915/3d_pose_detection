import cv2
import sys
import os
import importlib
from PoseDetectionModule import PoseDetection
import numpy as np

sys.path.append(os.path.realpath('../capture'))
SingleVideoFeedModule = importlib.import_module(
    'SingleVideoFeedModule', 'capture')

video = SingleVideoFeedModule.SingleVideoFeed(
    'C:/Users/Bence_Balogh/Desktop/3d_cam_proj/recordings/recording_1642535760245_ch_1.avi')
detector = PoseDetection(True)

prevFrame = None
while(True):
    frames = video.getFrames()
    frame = frames[0]

    if frame is None:
        frame = prevFrame

    detection = detector.getPositions([frame])

    displayFrame = np.rot90(detection['frames'][0], -1)

    cv2.imshow('frame', displayFrame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    prevFrame = frame

cv2.destroyAllWindows()
