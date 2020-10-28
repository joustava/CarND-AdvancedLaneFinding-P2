import cv2
import numpy


class Thresholder(object):
    """

    """

    def _channels(self, image):
        """
        Convert to HLS color space and separate the channels
        """
        hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        return (hls[:, :, 0], hls[:, :, 1], hls[:, :, 2])

    def _color(self, channel, threshold):
        # Threshold color channel
        binary = numpy.zeros_like(channel)
        binary[(channel >= threshold[0]) & (channel <= threshold[1])] = 1
        return binary

        # Stack each channel
    def _gradientx(self, channel, threshold):
        """

        """
        # Take the derivative in x
        sobelx = cv2.Sobel(channel, cv2.CV_64F, 1, 0)
        # Absolute x derivative to accentuate lines away from horizontal
        abs_sobelx = numpy.absolute(sobelx)
        scaled_sobel = numpy.uint8(255*abs_sobelx/numpy.max(abs_sobelx))
        # Threshold x gradient
        thresholded = numpy.zeros_like(scaled_sobel)
        thresholded[(scaled_sobel >= threshold[0]) &
                    (scaled_sobel <= threshold[1])] = 1

        return thresholded

    def threshold(self, image, s_thresh=(170, 255), sx_thresh=(20, 100)):
        """
        Apply color and gradient thresholding on an image.

        :param: image an undistorted image
        """
        image = numpy.copy(image)
        # TODO: check if blurring gives improvment.
        # image = cv2.GaussianBlur(image, (5, 5), 0)
        #   image = cv2.medianBlur(image, 5)
        h, l, s = self._channels(image)

        gradient_thresholded = self._gradientx(l, sx_thresh)
        color_thresholded = self._color(s, s_thresh)

        color_binary = numpy.dstack(
            (numpy.zeros_like(gradient_thresholded), gradient_thresholded, color_thresholded)) * 255

        color_binary[(gradient_thresholded != 0) |
                     (color_thresholded != 0)] = 255
        # color_binary[]

        return color_binary  # cv2.cvtColor(color_binary, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    image = cv2.imread('./assets/output_images/test5_undistorted_example.jpg')
    thr = Thresholder()
    mask = thr.threshold(image)
    cv2.imwrite('./assets/output_images/test5_undistorted_thresholded.jpg', mask)
