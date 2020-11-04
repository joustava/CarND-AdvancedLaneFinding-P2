import cv2
import numpy
from common.roi import Roi


class Transformer(object):

    def warp(self, binary):
        height, width = binary.shape[:2]

        src = Roi.src_corners(width, height)
        dst = Roi.dst_corners(width, height)

        M = cv2.getPerspectiveTransform(src, dst)
        Minv = cv2.getPerspectiveTransform(dst, src)

        # return binary and inverse transformation matrix
        return cv2.warpPerspective(binary, M, (width, height), flags=cv2.INTER_LINEAR), Minv
