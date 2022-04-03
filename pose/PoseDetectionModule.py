import cv2
from mediapipe.python.solutions import pose


class PoseDetection:
    def __init__(self):
        self.pose = pose.Pose(model_complexity=1)

    def getPose(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = self.pose.process(rgb)
        if pose is None or pose.pose_landmarks is None:
            return None
        return pose.pose_landmarks
