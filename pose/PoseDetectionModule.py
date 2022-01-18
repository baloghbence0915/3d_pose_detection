import cv2
from mediapipe.python.solutions import pose, drawing_utils
import numpy as np


class PoseDetection:
    def __init__(self, drawLandmarks=False):
        self.drawLandmarks = drawLandmarks
        self.pose = pose.Pose()

    def getPositions(self, frames):
        res = {"positions": [None, None], "frames": [None, None]}

        for i, frame in enumerate(frames):
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            positions = self.pose.process(imgRGB)

            if positions.pose_landmarks:
                res["positions"][i] = positions

                if self.drawLandmarks == True:
                    copyFrame = np.array(frame)
                    drawing_utils.draw_landmarks(
                        copyFrame, positions.pose_landmarks, pose.POSE_CONNECTIONS)
                    res["frames"][i] = copyFrame

        return res
