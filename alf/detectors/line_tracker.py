import numpy as np
import cv2

# LAneTracker
# MarkingDetector


class LineTracker(object):
    """
    Horizontal sliding window
    """

    def __init__(self, image, center_x, top_y, margin=100, height=100):
        self.minpix = 50
        self.max_height = image.shape[0]
        nonzero = image.nonzero()
        self.nonzeroy = np.array(nonzero[0])
        self.nonzerox = np.array(nonzero[1])
        self.margin = margin
        self.height = height
        self.top_y = top_y
        self._center_x = center_x
        self.indices = []

        self._center_x = center_x
        self.top_left = (center_x - margin, top_y)
        self.bottom_right = (center_x + margin, top_y + height)

    def track(self, pos):
        y = self.max_height - (pos + 1) * self.height
        self._slide(y)
        self.indices.append(self._marker_inds())

    def good_pixels(self):
        good_indices = np.concatenate(self.indices)
        return (self.nonzerox[good_indices], self.nonzeroy[good_indices])

    def draw(self, image, color=(0, 255, 0), thickness=2):
        """
        Helper for visualizing current window rectangles on the image
        """
        cv2.rectangle(image, self.top_left,
                      self.bottom_right, color, thickness)

    def _slide(self, y):
        """
        Track/Slide the window when needed.
        """
        if len(self._marker_inds()) > self.minpix:
            self._center_x = np.int(
                np.mean(self.nonzerox[self._marker_inds()]))

        self.top_left = (self._center_x - self.margin, y)
        self.bottom_right = (self._center_x + self.margin,
                             y + self.height)

    def _marker_inds(self):
        """
        Returns the pixel indices of probable lane line markers of currenly windowed area
        """
        return (
            (self.nonzeroy >= self.top_left[1])
            & (self.nonzeroy < self.bottom_right[1])
            & (self.nonzerox >= self.top_left[0])
            & (self.nonzerox < self.bottom_right[0])
        ).nonzero()[0]
