from math import tan, atan, degrees, radians, sin, acos, sqrt, pi
from collections import deque
import csv
import itertools
from statistics import mean

PI_PER_2 = pi / 2
PI_PER_4 = pi / 4

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
    p1Length = sqrt((p1['x'] ** 2) + (p1['z'] ** 2) + (p1['y'] ** 2))
    p2Length = sqrt((p2['x'] ** 2) + (p2['z'] ** 2) + (p2['y'] ** 2))
    b = p1Length * p2Length
    return acos(a / b)


def getBodyAngle(points):
    if bool(points):
        left_shoulder = points[11]
        right_shoulder = points[12]
        x = right_shoulder['x'] - left_shoulder['x']
        z = right_shoulder['z'] - left_shoulder['z']

        return getAngle({'x': x, 'y': 0, 'z': z}, {'x': 0, 'y': 0, 'z': -1}) - PI_PER_2
    return 0



l = 20
queues = [deque([0, 0], 3), deque([0, 0], 3)]
peaks = [deque([0, 0, 0, 0], 4), deque([0, 0, 0, 0], 4)]
crosses = deque([False, False], 20)
# f = open('f1.csv', 'w')
# writer = csv.writer(f)

# counter = 0

filterThreshold = 0.1; # ~5-6°
def _filterAngles(v):
    return v if v > filterThreshold else 0

def _transformDomain(v):
    return v / pi

def _processCrosses(queues, crosses):
    def _isCrossing(p1, p2, c1, c2):
        if p1 is not None and p2 is not None:
            isInc1 = p1 < c1
            isInc2 = p2 < c2
            a = None
            b = None

            if isInc1 and not isInc2:
                a = { "p": p2, "c": c2 }
                b = { "p": p1, "c": c1 }
            elif not isInc1 and isInc2:
                a = { "p": p1, "c": c1 }
                b = { "p": p2, "c": c2 }
            else:
                return False

            return (b["c"] < a["p"] and b["c"] > a["c"]) or (b["p"] < a["p"] and b["p"] > a["c"]) or (b["p"] < a["p"] and b["c"] > a["c"])
        return False

    curr1 = queues[0][-1]
    curr2 = queues[1][-1]
    prev1 = queues[0][-2]
    prev2 = queues[1][-2]
    crosses.append(_isCrossing(prev1, prev2, curr1, curr2))

mode = 'down'
peak = 0
    
def _processPeaks(arr, width):
    def _isUp(arr, c):
        arr2 = list(itertools.islice(arr, max(len(arr)-width-1, 0)))
        arr2.append(c)
        avg = mean(arr2)
        return avg < arr2[-1]

    def isDown(arr, c):
        arr2 = list(itertools.islice(arr, max(len(arr)-width-1, 0)))
        arr2.append(c)
        avg = mean(arr2)
        return avg < arr2[0]

    def _processPeaks(arr, c):
        peaks.append(None)
        hasChanged = False

        if mode == 'down':
            if _isUp(arr, c):
                mode = 'up'
                hasChanged = True

        if mode == 'up':
            if c > peak:
                peak = c

            if isDown(arr, c) and not hasChanged:
                mode = 'down'
                peaks[peaks.length - 1] = peak
                peak = 0

v = 0
h = 0
a = -1 / 200

def getSpeed(points):
    global counter
    offset = 0.075
    if bool(points):
        for i, side in enumerate([[24, 26], [23, 25]]):
            q = queues[i]
            hip = points[side[0]]
            knee = points[side[1]]
            x = knee['x'] - hip['x']
            y = knee['y'] - hip['y']
            z = knee['z'] - hip['z']
            angle = getAngle({'x': x, 'y': y, 'z': z},{'x': 0, 'y': -1, 'z': 0})

            a,b = q[-1],q[-2]
            sum = a + b + _transformDomain(_filterAngles(angle))
            q.append(sum/3)

        _processCrosses(queues, crosses)

        idx = False
        try:
            idx = crosses.index(True)
        except:
            pass

        if idx:
            const leftPeak = leftPeak3[i] || 0
            const rightPeak = rightPeak3[i] || 0
            const peak = (leftPeak + rightPeak) / 2
            if (peak > 0) {
                if (h < (peak*12)) {
                    v = 0
                    h = peak * 10
                    crosses3Copy[quota] = 0
                }
            }
        }

        v += a
        h += v
        if (h < 0) {
            h = 0
            v = 0
        } 
        i++
        return [...p, h / 3];

        # if counter < 1500:
        #     writer.writerow([queues[0][-1], queues[1][-1]])
        #     if (counter % 100)==0:
        #         print(counter)
        # elif counter == 1500:
        #     print('Close f')
        #     f.close()
        # counter+=1


    return 0


def unwrapCoords(points, i):
    return points["left"][i]['x'], points["left"][i]['y'], points["right"][i]['x'], points["right"][i]['y']
