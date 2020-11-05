import cv2
import numpy


class ImageThresholder(object):
    """

    """

    def _hsl_channels(self, image):
        """
        Convert image to HLS color space and return the separate channels
        """
        hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        return cv2.split(hls)

    def _apply_color_threshold(self, channel, threshold):
        # Create an image of zeros (black) with the same shape and type as the given image.
        binary = numpy.zeros_like(channel)
        # Set those pixels that fall into the color threshold to 1 (white)
        binary[(channel >= threshold[0]) & (channel <= threshold[1])] = 1
        return binary

        # Stack each channel
    def _apply_gradient_threshold(self, channel, threshold):
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
        h, l, s = self._hsl_channels(image)

        gradient_thresholded_image = self._apply_gradient_threshold(
            l, sx_thresh)
        color_thresholded_image = self._apply_color_threshold(s, s_thresh)

        # Stack BGR values
        # R channel is all 0
        # B channel is all 255
        # G channel is all 255
        color_binary = numpy.dstack(
            (numpy.zeros_like(gradient_thresholded_image), gradient_thresholded_image, color_thresholded_image)) * 255

        # From grayscaled color input create a binary image where colored pixels in the color binary are set to white.
        grayscale = cv2.cvtColor(color_binary, cv2.COLOR_BGR2GRAY)
        grayscale[(gradient_thresholded_image != 0) |
                  (color_thresholded_image != 0)] = 255

        return grayscale
