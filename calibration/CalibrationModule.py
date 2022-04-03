# https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0

import cv2
from cv2 import undistort
import numpy as np
import glob

from config.ConfigModule import Config

images = glob.glob('*.jpg')

class Undistortion:

    def __init__(self):
        config = Config()
        undistortion = config.get()["camera"]["mods"]["all"]["undistortion"]

        dim = undistortion['DIM']
        k = undistortion['K']
        d = undistortion['D']

        DIM=(dim[0], dim[1])
        K=np.array(k)
        D=np.array(d)

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        self.map1 = map1
        self.map2 = map2

    def execute(self, img):
        try:
            return cv2.remap(img, self.map1, self.map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        except:
            print('CalibrationModule:\t' + str(img.shape))
            return img