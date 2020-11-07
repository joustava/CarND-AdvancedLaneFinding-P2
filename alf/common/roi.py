import numpy
from imutils import perspective


class Roi(object):
    @staticmethod
    def src_corners(width, height, k=0.65):
        """
        Creates the source points for a perspective transform.
        The point data is obtained manually by drawing a polygon with four corners
        that make the lines fit against the outlines of a square lane section of about
        10 * the dashed lane line length.

        The points are ordered clockwise:
            top-left, 
            top-right,
            bottom-right,
            bottom-left
        """
        points = numpy.float32([
            [205, height],
            [1120, height],
            [602, 444],
            [680, 444]
        ])

        return perspective.order_points(points)

    @staticmethod
    def dst_corners(width, height):
        """
        Creates the destination points for a perspective transform.

        These points are chosen so that they end up in a rectangular fashion.


        The points are ordered clockwise:
            top-left, 
            top-right,
            bottom-right,
            bottom-left
        """
        src = Roi.src_corners(width, height)
        offset = 100
        points = numpy.float32(src)
        points[0] = [src[3, 0] + 100, 0]
        points[1] = [src[2, 0] - 100, 0]
        points[2] = [src[2, 0] - 100, src[2, 1]]
        points[3] = [src[3, 0] + 100, src[3, 1]]

        return perspective.order_points(points)
