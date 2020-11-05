import cv2
import numpy
from common.roi import Roi


class PerspectiveTransformer(object):
    def __init__(self, example):
        height = example.shape[0]
        width = example.shape[1]

        src = Roi.src_corners(width, height)
        dst = Roi.dst_corners(width, height)

        self.dimensions = (width, height)
        self.M = cv2.getPerspectiveTransform(src, dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)

    def warp(self, binary):
        """
        Apply a perspective transform on a image
        """
        return cv2.warpPerspective(binary, self.M, self.dimensions, flags=cv2.INTER_LINEAR)

    def unwarp(self, warped):
        """
        Apply a inverse persepctive transform on a image
        """
        return cv2.warpPerspective(warped, self.Minv, self.dimensions, flags=cv2.INTER_LINEAR)
