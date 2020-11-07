import numpy as np
import cv2


class PixelTracker(object):
    """
    The PixelTracker uses a sliding-window approach to detect lane lines from an image.

    First from a binary thresholded image of a top down view of a lane (perspective transformed) as input, all non-zero
    (white) pixel indexes are found.

    An initial window is placed on the bottom of the image where its position is based on center_x, top_y, margin and height input.

    With each tracking operation a minimum amount of pixels is detected of which the mean x position is calculated to be used
    as the next center_x, y position is updated based on a scalar (amount of windows), and this repeats until we reach the
    top of the lane. At that point all pixel indexes that were detected are part of a probably lane line.

    """

    def __init__(self, image, center_x, margin=100, height=100):
        self._minpix = 50
        self._image = image
        self._max_height = image.shape[0]
        nonzero = image.nonzero()
        self._nonzeroy = np.array(nonzero[0])
        self._nonzerox = np.array(nonzero[1])
        self._margin = margin
        self._height = height
        self._center_x = center_x
        self._indices = []
        self._center_x = center_x
        self._top_left = None
        self._bottom_right = None

    def track(self, nwindows):
        """
        Each call will reposition the window along x and y axes, detect those indices of pixels that are white within its bounds
        and collect these until sno more windows are required.
        """
        for window in range(nwindows):
            y = self._max_height - (window + 1) * self._height
            self._set_bounds(y)
            self._slide(y)
            self.draw()
            self._indices.append(self._current_marker_inds())

    def good_pixels(self):
        """
        Returns the x and y pixel indices of the probable line.
        """
        good_indices = np.concatenate(self._indices)
        x = self._nonzerox[good_indices]
        y = self._nonzeroy[good_indices]
        self.fit = np.polyfit(y, x, 2)
        return self.fit

    def draw(self, color=(0, 255, 0), thickness=2):
        """
        Helper for visualizing current window rectangles on the image
        """
        current_indices = self._current_marker_inds()
        x = self._nonzerox[current_indices]
        y = self._nonzeroy[current_indices]

        self._image[y, x] = [255, 0, 0]

        cv2.rectangle(self._image, self._top_left,
                      self._bottom_right, color, thickness)

    def _set_bounds(self, y):
        """
        Update window boundaries
        """
        self._top_left = (self._center_x - self._margin, y)
        self._bottom_right = (self._center_x + self._margin, y + self._height)

    def _slide(self, y):
        """
        Move the window over the x axis when needed.
        """
        if len(self._current_marker_inds()) > self._minpix:
            self._center_x = np.int(
                np.mean(self._nonzerox[self._current_marker_inds()]))

    def _current_marker_inds(self):
        """
        Returns the pixel indices of probable lane line markers of currenly windowed area.
        The indices are the actual x and y values of white pixels.
        """
        return ((self._nonzeroy >= self._top_left[1])
                & (self._nonzeroy < self._bottom_right[1])
                & (self._nonzerox >= self._top_left[0])
                & (self._nonzerox < self._bottom_right[0])
                ).nonzero()[0]
