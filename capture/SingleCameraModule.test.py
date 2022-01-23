import cv2
from SingleCameraModule import SingleCamera

cam = SingleCamera(channel=0, requested_resolution=(1280,719), record=False)
i = 0
while(True):
    frame = cam.getFrame()
    # frame[:,int(frame.shape[1]/2)] = [0,0,255]
    # frame[int(frame.shape[0]/2),:] = [0,0,255]
    cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('img_'+ str(i) +'_1280_720.jpg', frame)
        i += 1
    
    if i == 9:
        break



cv2.destroyAllWindows()
