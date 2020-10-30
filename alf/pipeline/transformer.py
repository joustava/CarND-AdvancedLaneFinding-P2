import cv2
import numpy
from common.roi import Roi


class Transformer(object):

    def warp(self, binary):

        # shape = binary.shape
        height, width, _ = binary.shape

        src = Roi.src_corners(width, height)

        print(src)

        dst = Roi.dst_corners(width, height)

        print(dst)
        for idx, corner in enumerate(src):
            x, y = corner
            character = chr(48 + idx)
            cv2.circle(binary, (x, y), 10, color=(0, 0, 250), thickness=-1)
            cv2.putText(binary, character, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.line(binary, tuple(src[0]), tuple(src[1]), (0, 0, 250), 2)
        cv2.line(binary, tuple(src[1]), tuple(src[2]), (0, 0, 250), 2)
        cv2.line(binary, tuple(src[2]), tuple(src[3]), (0, 0, 250), 2)
        cv2.line(binary, tuple(src[3]), tuple(src[0]), (0, 0, 250), 2)

        for idx, corner in enumerate(dst):
            x, y = corner
            character = chr(48 + idx)
            cv2.circle(binary, (x, y), 10,
                       color=(250, 0, 0), thickness=-1)
            cv2.putText(binary, character, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (250, 0, 0), 2, cv2.LINE_AA)

        cv2.imwrite(
            './assets/output_images/test5_undistorted_marked.jpg', binary)

        # return binary
        M = cv2.getPerspectiveTransform(src, dst)
        Minv = cv2.getPerspectiveTransform(dst, src)

        # return binary
        return cv2.warpPerspective(binary, M, (width, height), flags=cv2.INTER_LINEAR)
