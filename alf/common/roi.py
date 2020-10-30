import numpy
from imutils import perspective

pos1 = (597, 450)  # (597, 450)   (527, 500)
pos2 = (687, 450)  # (687, 450) (757, 500)
pos3 = (1110, 719)
pos4 = (220, 719)


class Roi(object):
    @staticmethod
    def src_corners(width, height, k=0.65):
        """
        Creates the vertices to denote a region of interest.
        """
        offset = 160
        points = numpy.float32([
            (offset, height),
            (width - 130, height),
            (width//2 - 80, height * k),
            (width//2 + 100, height * k)
        ])

        return perspective.order_points(points)

    @staticmethod
    def dst_corners(width, height):
        src = Roi.src_corners(width, height)

        points = numpy.float32(src)
        points[0] = [src[3][0], 0]
        points[1] = [src[2][0], 0]
        points[2] = src[2]
        points[3] = src[3]

        return perspective.order_points(points)
