import cv2
import numpy
from common.lane import Lane
# WIP, DEPRECATED?


class CornerDetector(object):

    def __init__(self, n=4):
        """
        :number: corners you want to find
        """
        self._number = n

    def _draw_lines(self, image, lines, color=[255, 0, 0], thickness=1):
        """
        Renders lines upon the image.
        """
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    def find(self, binary):
        """
        Find n amount of corners in grayscale image

        :image: grayscale image
        quality level, which is a value between 0-1, which denotes the minimum quality of corner below which everyone is rejected.
        Then we provide the minimum euclidean distance between corners detected.
        """
        rho = 1            # distance resolution in pixels of the Hough grid
        theta = numpy.pi/180  # angular resolution in radians of the Hough grid
        threshold = 15     # minimum number of votes
        min_line_len = 15  # minimum number of pixels to concider as line
        # maximum pixel space between connectable line segments.
        max_line_gap = 1
        # print(binary.shape)

        gray = cv2.cvtColor(binary, cv2.COLOR_BGR2GRAY)

        height, width, _ = binary.shape

        lines = cv2.HoughLinesP(gray, rho, theta, threshold, numpy.array(
            []), minLineLength=min_line_len, maxLineGap=max_line_gap)
        markers = Lane.extrapolate(lines, width, height)
        self._draw_lines(binary, [markers])

        corners = Lane.extrapolate(lines, width, height)

        # # corners = cv2.goodFeaturesToTrack(binary, self._number, 0.01, 10)
        # # print(corners)
        # # corners = numpy.int0(corners)
        # # corners = sorted(numpy.concatenate(corners).tolist())

        for corner in corners:
            cv2.circle(binary, corner, 2, color=(0, 0, 250), thickness=-1)

        return binary
