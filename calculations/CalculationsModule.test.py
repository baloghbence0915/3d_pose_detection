from os import listdir
from os.path import isfile, join
import cv2
import numpy as np
from CalculationsModule import getAlpha, getBeta, getDist
from math import tan, radians

files = [f for f in listdir('images') if isfile(
    join('images', f)) and f.endswith('.png')]

data = dict()

for f in files:
    s = f.replace('.png', '')
    ss = s.split('_')
    dist = str(ss[1])
    id = str(ss[0])
    side = str(ss[2])

    if dist not in data:
        data[dist] = dict()

    if id not in data[dist]:
        data[dist][id] = dict()

    if side not in data[dist][id]:
        data[dist][id][side] = dict()

    data[dist][id][side]['img'] = cv2.imread(join('images', f), 0)

mouseX = 0
mouseY = 0


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY, clicked
    mouseX, mouseY = x, y


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

for dist in data:
    for id in data[dist]:
        for side in data[dist][id]:
            img = data[dist][id][side]['img']
            clicked = False
            print('Side: ' + side)
            while(True):
                cv2.imshow('image', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    data[dist][id][side]['x'] = mouseX / img.shape[1]
                    data[dist][id][side]['img'] = None
                    break

        phi = 62
        alpha = getAlpha(data[dist][id]['l']['x'], phi)
        beta = getBeta(data[dist][id]['r']['x'], phi)
        print(str(phi))
        print(str(alpha))
        print(str(beta))
        span = 140
        distance = getDist(alpha, beta, span)
        print('Dist: ' + str(dist) + '\t' + 'Approx.: ' + str(distance))
