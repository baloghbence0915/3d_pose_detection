import cv2
from capture.SingleVideoFeedModule import SingleVideoFeed
from pose.PoseDetectionModule import PoseDetection

video = SingleVideoFeed('C:/Users/Bence_Balogh/Desktop/3d_cam_proj/recordings/recording_1641928970890_ch_0.avi')
detector = PoseDetection(True)

prevFrame = None
while(True):
    frames = video.getFrames()
    frame = frames[0]

    if frame is None:
        frame = prevFrame

    detection = detector.getPositions([frame])

    cv2.imshow('frame', detection["frames"][0])

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    prevFrame = frame

cv2.destroyAllWindows()
