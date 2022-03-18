from math import tan, atan, degrees, radians, sin, acos, sqrt, asin


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


def get_body_angle(points):
    if bool(points):
        left_shoulder = points[11]
        right_shoulder = points[12]
        x = right_shoulder['x'] - left_shoulder['x']
        z = right_shoulder['z'] - left_shoulder['z']

        return acos(x / sqrt(pow(x, 2) + pow(z, 2))) * (1 if z >= 0 else -1)

    return 0


def get_speed(points):

    if bool(points):
        angles = []
        for side in [[24, 26], [23, 25]]:
            hip = points[side[0]]
            knee = points[side[1]]
            x = knee['x'] - hip['x']
            y = knee['y'] - hip['y']
            z = knee['z'] - hip['z']
            angle = acos(-y / sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)))
            angles.append(angle)

        return angles

    return [0, 0]
