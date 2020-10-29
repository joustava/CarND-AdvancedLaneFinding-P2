# Define a class to receive the characteristics of each line detection
import numpy


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
        self.current_fit = [numpy.array([False])]
        # radius of curvature of the line in some units
        self.radius_of_curvature = None
        # distance in meters of vehicle center from the line
        self.line_base_pos = None
        # difference in fit coefficients between last and new fits
        self.diffs = numpy.array([0, 0, 0], dtype='float')
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.ally = None

    @staticmethod
    def extrapolate(center, slope, height, k=0.6):
        """
        Calculate the desired start and end points from a given center point and slope with linear equation:

            y = mx + b

        Height is y axis maximum, k a scaling constant to be able to control where the line stops.
        """
        x, y = center
        b = y - slope * x

        x1 = (height - b) / slope
        x2 = (height * k - b) / slope

        return [x1, height, x2, height * k]
