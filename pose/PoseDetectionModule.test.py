import cv2
import sys
import os
import importlib
from PoseDetectionModule import PoseDetection
import numpy as np
from os.path import join

sys.path.append(os.path.realpath('../capture'))
SingleVideoFeedModule = importlib.import_module(
    'SingleVideoFeedModule', 'capture')
SingleCameraModule = importlib.import_module(
    'SingleCameraModule', 'capture')

detector = PoseDetection(True)
video = SingleCameraModule.SingleCamera(0, requested_resolution=(1280,719))

while(True):
    frame = video.getFrame()
    pos, landmarks = detector.getPositions(frame)
    cv2.imshow('landmarks', landmarks)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

video = SingleVideoFeedModule.SingleVideoFeed(join('..', 'recordings', 'recording_1642535760245_ch_1.avi'))
prevFrame = None

while(True):
    frame = video.getFrame()

    if frame is None:
        frame = prevFrame

    pos, landmarks = detector.getPositions(frame)

    landmarks = np.rot90(landmarks, -1)

    cv2.imshow('landmarks', landmarks)

    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

    prevFrame = frame

cv2.destroyAllWindows()
