import numpy as np
import cv2
from .line_tracker import PixelTracker
from common.line import Line

# Based on 'Lesson 8: Advanced Computer Vision - 4. Finding the Lines: Sliding Window


class LaneDetector(object):
    def __init__(self):
        self.nwindows = 15
        self.LEFT = Line()
        self.RIGHT = Line()

    def _find_lane_base(self, binary_warped):
        """
        Find the base x axis value of the left and right lane markings
        by applying a Histogram over the y direction of the bottom half
        of a binary and warped image.
        """
        histogram = np.sum(
            binary_warped[binary_warped.shape[0]//2:, :], axis=0)

        half = np.int(histogram.shape[0]//2)
        left_line_x = np.argmax(histogram[:half])
        right_line_x = np.argmax(histogram[half:]) + half

        return (left_line_x, right_line_x)

    def _polynomial(self, polyfit, y):
        A, B, C = polyfit
        return A * y ** 2 + B * y + C

    def radius(self, y, polyfit, ym_per_pix=1.0):
        """
        With the coefficients we found by fitting the polynomial we can find the xs
        """
        A, B = polyfit[:2]
        return ((1 + (2 * A * y * ym_per_pix + B) ** 2) ** 1.5) / np.absolute(2 * A)

    def fill_lane(self, image, leftx, rightx, ploty):
        """
        Fills area between two lines.
        From: Tips and tricks for the Project
        """
        window = np.zeros_like(image)
        pts_left = np.array([np.transpose(np.vstack([leftx, ploty]))])
        pts_right = np.array(
            [np.flipud(np.transpose(np.vstack([rightx, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(window, np.int_([pts]), (0, 255, 0))
        return cv2.addWeighted(image, 1, window, 0.3, 0)

    def track_lines(self, image):
        """
        On on image binary we apply a windowed search from the bottom of
        the screen for both left and right lane lines.
        """
        out_img = np.dstack((image, image, image))

        if self.LEFT.detected and self.RIGHT.detected:
            pass
        else:
            # Set height of windows - based on nwindows above and image shape
            height = np.int(image.shape[0]//self.nwindows)

            # Current positions to be updated later for each window in nwindows
            left_line_x, right_line_x = self._find_lane_base(image)

            # Initialize sliding windows to track both left and right lane markers
            left_window = PixelTracker(out_img,
                                       center_x=left_line_x, height=height)
            right_window = PixelTracker(out_img,
                                        center_x=right_line_x, height=height)

            left_window.track(self.nwindows)
            right_window.track(self.nwindows)

            # Extract left and right line pixel positions
            self.LEFT.current_fit = left_fit = left_window.good_pixels()
            self.RIGHT.current_fit = right_fit = right_window.good_pixels()
            return left_fit, right_fit, out_img

    def detect(self, binary):
        """
        Detects and plots the lane line marking.
        """
        # The lane will be visualized on this canvas
        lane_image = np.dstack((binary, binary, binary))
        lane_image[:, :] = [0, 0, 0]

        # Generate y values over the whole height range.
        ploty = np.linspace(0, binary.shape[0]-1, binary.shape[0])

        # Calculate polyfits for both lines
        left_fit, right_fit, annotated_image = self.track_lines(binary)

        try:
            # Calculate x values
            left_fitx = self._polynomial(left_fit, ploty)
            right_fitx = self._polynomial(right_fit, ploty)
        except TypeError:
            # Avoids an error if `left` and `right_fit` are still none or incorrect
            print('The function failed to fit a line!')
            left_fitx = 1 * ploty**2 + 1 * ploty
            right_fitx = 1*ploty**2 + 1 * ploty

        left_curve = np.column_stack(
            (left_fitx.astype(np.int32), ploty.astype(np.int32)))
        right_curve = np.column_stack(
            (right_fitx.astype(np.int32), ploty.astype(np.int32)))

        cv2.polylines(lane_image, [left_curve],
                      isClosed=False, color=(0, 255, 255), thickness=25)
        cv2.polylines(lane_image, [right_curve], isClosed=False,
                      color=(0, 255, 250), thickness=25)

        cv2.polylines(annotated_image, [left_curve],
                      isClosed=False, color=(0, 255, 255), thickness=3)
        cv2.polylines(annotated_image, [right_curve], isClosed=False,
                      color=(0, 255, 255), thickness=3)

        lane_image = self.fill_lane(lane_image, left_fitx, right_fitx, ploty)

        y = np.max(ploty)
        rl = self.radius(y, left_fit)
        rr = self.radius(y, right_fit)

        return lane_image, annotated_image, left_curve, right_curve, rl, rr
