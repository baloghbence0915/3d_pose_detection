import cv2
import sys
import os
import importlib
from CalibrationModule import Undistortion

sys.path.append(os.path.realpath('../capture'))
SingleCameraModule = importlib.import_module(
    'SingleCameraModule', 'capture')

video = SingleCameraModule.SingleCamera(0, requested_resolution=(1280,719))
undistortion = Undistortion()

while(True):
    frame = video.getFrame()
    # cv2.imshow('landmarks', frame)
    cv2.imshow('landmarks', undistortion.execute(frame))

    if cv2.waitKey(50) & 0xFF == ord('q'):
        print(frame.shape)
        break
