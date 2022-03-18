from turtle import position
import cv2
from mediapipe.python.solutions import pose, drawing_utils
import numpy as np


class PoseDetection:
    def __init__(self, drawLandmarks=False):
        self.drawLandmarks = drawLandmarks
        self.pose = pose.Pose(model_complexity=1)

    def getPositions(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        positions = self.pose.process(rgb)
        landmarks = frame 

        if positions.pose_landmarks and self.drawLandmarks == True:
            copyFrame = np.array(frame)
            drawing_utils.draw_landmarks(
                copyFrame, positions.pose_landmarks, pose.POSE_CONNECTIONS)
            landmarks = copyFrame

        return (positions, landmarks)
