import cv2
from SingleCameraModule import SingleCamera

cam = SingleCamera(channel=1, record=True)

while(True):
    frames = cam.getFrames()
    frame = frames[0]
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
