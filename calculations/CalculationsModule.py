from math import tan, atan, degrees, radians, sin


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
    return tan(radians(slope)) * x + bias
