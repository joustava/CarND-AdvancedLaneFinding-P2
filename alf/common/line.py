# Define a class to receive the characteristics of each line detection
import numpy as np


class Line():
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False
        # x values of the last n fits of the line
        self.recent_xfitted = []
        # average x values of the fitted line over the last n iterations
        self.bestx = None
        # polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        # radius of curvature of the line in some units
        self.radius_of_curvature = None
        # distance in meters of vehicle center from the line
        self.line_base_pos = None
        # difference in fit coefficients between last and new fits
        self.diffs = np.array([0, 0, 0], dtype='float')
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.ally = None
        self._nonzeroy = None
        self._nonzerox = None

    def search_around(self, image, margin=50):
        nonzero = image.nonzero()
        self._nonzeroy = np.array(nonzero[0])
        self._nonzerox = np.array(nonzero[1])

        indices = self.indices()

        self.allx = self._nonzerox[indices]
        self.ally = self._nonzeroy[indices]

        self.draw(image)
        return np.polyfit(self.ally, self.allx, 2)

    def indices(self):
        A, B, C = self.current_fit
        y = self._nonzeroy
        x = self._nonzerox
        margin = 50
        return ((x > (A*(y**2) + B*y + C - margin)) & (x < (A*(y**2) + B*y + C + margin)))

    def draw(self, image):
        # Generate y values over the whole height range.
        ploty = np.linspace(0, image.shape[0]-1, image.shape[0])
        window = np.zeros_like(image)
        pts_left = np.array([np.transpose(np.vstack([self.allx, ploty]))])
        pts_right = np.array(
            [np.flipud(np.transpose(np.vstack([self.ally, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(window, np.int_([pts]), (0, 255, 0))
        return cv2.addWeighted(image, 1, window, 0.3, 0)
