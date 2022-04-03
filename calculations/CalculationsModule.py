from math import tan, atan, degrees, radians, sin, acos, sqrt, pi
from collections import deque
import csv

PI_PER_2 = pi / 2

def getAlpha(x, phi):
    m = 0.5 / tan(radians(phi / 2))

    if x < 0.0 or x > 1.0:
        raise Exception('Wrong value for alpha')
    elif x <= 0.5:
        return ((180 - phi) / 2) + phi - ((phi / 2) - degrees(atan((0.5 - x) / m)))
    elif x > 0.5:
        return ((180 - phi) / 2) + phi - ((phi / 2) + degrees(atan((x - 0.5) / m)))


def getBeta(x, phi):
    m = 0.5 / tan(radians(phi / 2))

    if x < 0.0 or x > 1.0:
        raise Exception('Wrong value for beta')
    elif x <= 0.5:
        return ((180 - phi) / 2) + (phi / 2) - degrees(atan((0.5 - x) / m))
    elif x > 0.5:
        return ((180 - phi) / 2) + (phi / 2) + degrees(atan((x - 0.5) / m))


def __getDist(alpha, beta, span):
    gamma = 180 - alpha - beta
    if sin(radians(gamma)) == 0:
        return 0

    return sin(radians(alpha)) * ((span * sin(radians(beta))) / sin(radians(gamma)))


def getDistanceOfPoint(a, b, angle, baseline, scale):
    distance = 0

    try:
        alpha = getAlpha(a, angle)
        beta = getBeta(b, angle)
        distance = __getDist(alpha, beta, baseline) * scale
    except:
        pass

    return distance


def linearFn(x, slope, bias):
    return (tan(radians(slope)) * x) + bias


def getAngle(p1, p2):
    a = (p1['x'] * p2['x']) + (p1['y'] * p2['y']) + (p1['z'] * p2['z'])
    b = sqrt((p1['x'] ** 2) + (p1['z'] ** 2) + (p1['y'] ** 2)) + \
        sqrt((p1['x'] ** 2) + (p1['z'] ** 2) + (p1['y'] ** 2))
    return acos(a/b)


def getBodyAngle(points):
    if bool(points):
        left_shoulder = points[11]
        right_shoulder = points[12]
        x = right_shoulder['x'] - left_shoulder['x']
        z = right_shoulder['z'] - left_shoulder['z']

        return getAngle({'x': x, 'y': 0, 'z': z}, {'x': 0, 'y': 0, 'z': -1}) - PI_PER_2
        # return x / sqrt(pow(x, 2) + pow(z, 2))
        # * (1 if z >= 0 else -1)

    return 0



l = 20
queues = [deque([], l), deque([], l)]
test = deque([], l)
# f = open('f1.csv', 'w')
# writer = csv.writer(f)

# counter = 0


def getSpeed(points):
    # global counter
    offset = 0.075
    if bool(points):
        for i, side in enumerate([[24, 26], [23, 25]]):
            hip = points[side[0]]
            knee = points[side[1]]
            x = knee['x'] - hip['x']
            y = knee['y'] - hip['y']
            z = knee['z'] - hip['z']
            angle = getAngle({'x': x, 'y': y, 'z': z},{'x': 0, 'y': -1, 'z': 0})
            queues[i].append((angle - offset) if angle > offset else 0)

        # if counter < 1000:
        #     writer.writerow([queues[0][-1], queues[1][-1]])
        # elif counter == 1000:
        #     print('Close f')
        #     f.close()
        # counter+=1

        avg = []
        for q in queues:
            sum = 0
            for val in q:
                sum += val
            avg.append(sum/l)

        test.append(avg[0] * avg[1] * 500)

        sum = 0
        for val in test:
            sum += val
        avg = sum/l
        return avg if avg < 1 else 1

    return 0


def unwrapCoords(points, i):
    return points["left"][i]['x'], points["left"][i]['y'], points["right"][i]['x'], points["right"][i]['y']
