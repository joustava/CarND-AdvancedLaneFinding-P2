import cv2


class Transformer(object):
    def warp(self, image, src, dst):
        M = cv2.getPerspectiveTransform(src, dst)
        # Minv = cv2.getPerspectiveTransform(dst, src)

        height, width, _ = image.shape
        cv2.warpPerspective(image, M, (height, width), flags=cv2.INTER_LINEAR)
