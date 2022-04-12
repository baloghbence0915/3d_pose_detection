from math import tan, atan, degrees, radians, sin, acos, sqrt, pi, cos

from calculations.SpeedModule import Speed

PI_PER_2 = pi / 2

def getSubAngleOfTriangular(a, gamma, x):
    b = (a/2) / sin(radians(gamma)/2)
    lambd = (180-gamma)/2
    c = sqrt((b**2) + (x**2) - (2*b*x*cos(radians(lambd))))
    fi = degrees(acos(((b**2)+(c**2)-(x**2))/(2*b*c)))
    return fi

def getAlpha(x, gamma):
    if x < 0.0 or x > 1.0:
        raise Exception('Wrong value for alpha')

    return getSubAngleOfTriangular(1, gamma, 1-x) + ((180-gamma)/2)


def getBeta(x, gamma):
    if x < 0.0 or x > 1.0:
        raise Exception('Wrong value for beta')

    return getSubAngleOfTriangular(1, gamma, x) + ((180-gamma)/2)


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
    global PI_PER_2
    if bool(points):
        left_shoulder = points[11]
        right_shoulder = points[12]
        x = right_shoulder['x'] - left_shoulder['x']
        z = right_shoulder['z'] - left_shoulder['z']

        return getAngle({'x': x, 'y': 0, 'z': z}, {'x': 0, 'y': 0, 'z': -1}) - PI_PER_2
    return 0


speed = Speed()


def getSpeed(points):
    global speed
    if bool(points):
        for i, idx in enumerate([[24, 26], [23, 25]]):
            hip = points[idx[0]]
            knee = points[idx[1]]
            x = knee['x'] - hip['x']
            y = knee['y'] - hip['y']
            z = knee['z'] - hip['z']
            angle = getAngle({'x': x, 'y': y, 'z': z},
                             {'x': 0, 'y': -1, 'z': 0})
            speed.addAngle('left' if i == 0 else 'right', angle)

    return speed.getSpeed()


def unwrapCoords(points, i):
    return points["left"][i]['x'], points["left"][i]['y'], points["right"][i]['x'], points["right"][i]['y']
