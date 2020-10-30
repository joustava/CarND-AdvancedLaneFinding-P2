import numpy
from .line import Line


class Lane(object):
    @staticmethod
    def extrapolate(lines, width, height):
        """
        Extrapolating the left and right road marker (Hough) data
        """
        rm = []
        lm = []
        rc = []
        lc = []

        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2-y1)/(x2-x1)
                center = [(x1 + x2)/2, (y1 + y2)/2]
                if (slope < -0.5):
                    lm.append(slope)
                    lc.append(center)
                elif(slope > 0.5):
                    rm.append(slope)
                    rc.append(center)

        r_slope = numpy.sum(rm)/len(rm)
        l_slope = numpy.sum(lm)/len(lm)

        r_center = numpy.divide(numpy.sum(rc, axis=0), len(rc))
        l_center = numpy.divide(numpy.sum(lc, axis=0), len(lc))

        right = Line.extrapolate(r_center, r_slope, height)
        left = Line.extrapolate(l_center, l_slope, height)

        return numpy.array([left, right], dtype=numpy.int)
