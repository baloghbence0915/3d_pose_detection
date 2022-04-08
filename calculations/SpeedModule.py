
from collections import deque
import csv
from math import pi
from statistics import mean


class Speed:
    def __init__(self, anglesLength=3, peaksLength=4, crossesLength=20):
        self.leftAngles = deque([0]*anglesLength, anglesLength)
        self.rightAngles = deque([0]*anglesLength, anglesLength)
        self.leftMagnitudes = deque([0]*peaksLength, peaksLength)
        self.rightMagnitudes = deque([0]*peaksLength, peaksLength)
        self.leftPeaks = deque([0]*peaksLength, peaksLength)
        self.leftPeakProcess = Peaks(self.leftMagnitudes, self.leftPeaks)
        self.rightPeaks = deque([0]*peaksLength, peaksLength)
        self.rightPeakProcess = Peaks(self.rightMagnitudes, self.rightPeaks)
        self.crosses = deque([False]*crossesLength, crossesLength)

        self.v = 0
        self.h = 0
        self.a = -1 / 200

        self.filterThreshold = 0.1  # ~5-6°
        self.counter = 0
        # self.f = open('f2.csv', 'w')
        # self.writer = csv.writer(self.f)

    def addAngle(self, side, angle):
        angles = None
        magnitudes = None
        peakProcess = None

        if side == 'left':
            angles = self.leftAngles
            magnitudes = self.leftMagnitudes
            peakProcess = self.leftPeakProcess
        elif side == 'right':
            angles = self.rightAngles
            magnitudes = self.rightMagnitudes
            peakProcess = self.rightPeakProcess

        angles.append(self._transformDomain(self._filterAngles(angle)))
        magnitudes.append(mean(angles))
        peakProcess.processPeaks()

    def getSpeed(self):
        self._processCrosses()

        # if self.counter < 1500:
        #     self.writer.writerow([self.counter, 'leftAngle', self.leftAngles[-1]])
        #     self.writer.writerow([self.counter, 'rightAngle', self.rightAngles[-1]])
        #     self.writer.writerow([self.counter, 'leftMagnitude', self.leftMagnitudes[-1]])
        #     self.writer.writerow([self.counter, 'rightMagnitude', self.rightMagnitudes[-1]])
        #     self.writer.writerow([self.counter, 'leftPeak', self.leftPeaks[-1]])
        #     self.writer.writerow([self.counter, 'rightPeak', self.rightPeaks[-1]])
        #     self.writer.writerow([self.counter, 'cross', 0.5 if self.crosses[-1] else 0])
        #     if (self.counter % 100)==0:
        #         print(self.counter)
        # elif self.counter == 1500:
        #     print('Close f')
        #     self.f.close()
        # self.counter+=1

        quota = None
        try:
            quota = self.crosses.index(True)
        except:
            pass

        if quota is not None:
            peak = (self.leftPeaks[-1] + self.rightPeaks[-1]) / 2
            if peak > 0.0:
                if self.h < peak*12:
                    self.v = 0
                    self.h = peak * 10
                    self.crosses[quota] = False

        self.v += self.a
        self.h += self.v
        if self.h < 0.0:
            self.h = 0
            self.v = 0

        res = self.h/3

        return res

    def _processCrosses(self):
        p1 = self.leftMagnitudes[-2]
        p2 = self.rightMagnitudes[-2]
        c1 = self.leftMagnitudes[-1]
        c2 = self.rightMagnitudes[-1]
        self.crosses.append(self._isCrossing(p1, p2, c1, c2))

    def _filterAngles(self, v):
        return v if v > self.filterThreshold else 0

    def _transformDomain(self, v):
        return v / pi

    def _isCrossing(self, p1, p2, c1, c2):
        if p1 is not None and p2 is not None:
            isInc1 = p1 < c1
            isInc2 = p2 < c2
            a = None
            b = None
            c = None
            d = None

            if isInc1 and not isInc2:
                a = {"p": p2, "c": c2}
                b = {"p": p1, "c": c1}
            elif not isInc1 and isInc2:
                a = {"p": p1, "c": c1}
                b = {"p": p2, "c": c2}
            else:
                return False

            return (b["c"] < a["p"] and b["c"] > a["c"]) or (b["p"] < a["p"] and b["p"] > a["c"]) or (b["p"] < a["p"] and b["c"] > a["c"])
        return False


class Peaks:
    def __init__(self, magnitudes, peaks):
        self.mode = 'down'
        self.peak = 0.0
        self.magnitudes = magnitudes
        self.peaks = peaks

    def processPeaks(self):
        self.peaks.append(0)
        hasChanged = False
        magnitude = self.magnitudes[-1]

        if self.mode == 'down' and self._isUp():
            self.mode = 'up'
            hasChanged = True

        if self.mode == 'up':
            if magnitude > self.peak:
                self.peak = magnitude

            if self._isDown() and not hasChanged:
                self.mode = 'down'
                self.peaks[-1] = self.peak
                self.peak = 0

    def _isUp(self):
        avg = mean(self.magnitudes)
        return avg < self.magnitudes[-1]

    def _isDown(self):
        avg = mean(self.magnitudes)
        return avg < self.magnitudes[0]
