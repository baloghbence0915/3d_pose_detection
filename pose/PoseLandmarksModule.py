from mediapipe.python.solutions import drawing_utils
from mediapipe.python.solutions.pose import POSE_CONNECTIONS
import numpy as np


def drawLandmarks(frame, pose):
    if pose is not None:
        drawing_utils.draw_landmarks(
            frame, pose, POSE_CONNECTIONS)
