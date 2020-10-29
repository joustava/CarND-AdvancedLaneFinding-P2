import cv2
import numpy


class Transformer(object):

    def warp(self, binary, src, dst):

        # corners = cv2.goodFeaturesToTrack(binary)
        # corners = numpy.int0(corners)
        # corners = sorted(numpy.concatenate(corners).tolist())

        # for corner in corners:
        #     cv2.circle(binary, corner, 5, color=(0, 0, 250), thickness=-1)

        return binary
        # M = cv2.getPerspectiveTransform(src, dst)
        # # Minv = cv2.getPerspectiveTransform(dst, src)

        # height, width, _ = image.shape
        # cv2.warpPerspective(image, M, (height, width), flags=cv2.INTER_LINEAR)


if __name__ == "__main__":
    gray = cv2.imread(
        './assets/outout_images/test5_undistorted_thresholded.py')

    tr = Transformer()
    # tr.warp(gray)
