# https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0

import cv2
import numpy as np
import os
import glob

images = glob.glob('*.jpg')

DIM=(1280, 720)
K=np.array([[968.7993688992763, 0.0, 636.6769644053292], [0.0, 968.1174917158764, 371.2578003431906], [0.0, 0.0, 1.0]])
D=np.array([[-0.06072065680960785], [-0.6138856994344386], [2.7087538472302595], [-4.572162434753327]])

def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for p in images:
        undistort(p)