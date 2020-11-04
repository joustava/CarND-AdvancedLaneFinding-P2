import numpy as np
import cv2
from .sliding_window import SlidingWindow

# Based on 'Lesson 8: Advanced Computer Vision - 4. Finding the Lines: Sliding Window


class LaneDetector(object):
    def __init__(self):
        self.nwindows = 9

    def find_lane_base(self, binary_warped):
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

    def find_lane_pixels(self, binary_warped):
        # Create an output image to draw on and visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.shape[0]//self.nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated later for each window in nwindows
        left_line_x, right_line_x = self.find_lane_base(
            binary_warped)

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Initialize sliding windows to track both left and right lane markers
        left_window = SlidingWindow(binary_warped,
                                    center_x=left_line_x, top_y=window_height * self.nwindows - window_height, height=window_height)
        right_window = SlidingWindow(binary_warped,
                                     center_x=right_line_x, top_y=window_height * self.nwindows - window_height, height=window_height)

        # Step through the windows one by one and update left and right left and right lane marker trackers
        for window in range(self.nwindows):
            # Track line with current window
            left_window.track(window)
            right_window.track(window)

            # Visualize results
            left_window.draw(out_img)
            right_window.draw(out_img)

            # Extract lane marker pixels
            good_left_inds = left_window.marker_inds()
            good_right_inds = right_window.marker_inds()

            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        try:
            left_lane_inds = np.concatenate(left_lane_inds)
            right_lane_inds = np.concatenate(right_lane_inds)
        except ValueError:
            # Avoids an error if the above is not implemented fully
            pass

        # Extract left and right line pixel positions

        # leftx, lefty = left_window.extract()
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        return leftx, lefty, rightx, righty, out_img

    def curve(y, polyfit, ym_per_pix=1):
        return ((1 + (2*polyfit[0]*y*ym_per_pix + polyfit[1])**2)**1.5) / np.absolute(2*polyfit[0])

    def fit_polynomial(self, binary_warped, ym_per_pix=1, xm_per_pix=1):
        # Find our lane pixels first
        leftx, lefty, rightx, righty, out_img = self.find_lane_pixels(
            binary_warped)

        # Fit a second order polynomial to each using `np.polyfit`
        left_fit = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, 2)
        right_fit = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, 2)

        # Generate x and y values for plotting
        ploty = np.linspace(
            0, binary_warped.shape[0]-1, binary_warped.shape[0])
        try:
            left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
            right_fitx = right_fit[0]*ploty**2 + \
                right_fit[1]*ploty + right_fit[2]
        except TypeError:
            # Avoids an error if `left` and `right_fit` are still none or incorrect
            print('The function failed to fit a line!')
            left_fitx = 1*ploty**2 + 1*ploty
            right_fitx = 1*ploty**2 + 1*ploty

        # Visualization ##
        # Colors in the left and right lane regions
        out_img[lefty, leftx] = [255, 0, 0]
        out_img[righty, rightx] = [0, 0, 255]

        # Plots the left and right polynomials on the lane lines
        left_curve = np.column_stack(
            (left_fitx.astype(np.int32), ploty.astype(np.int32)))
        right_curve = np.column_stack(
            (right_fitx.astype(np.int32), ploty.astype(np.int32)))

        cv2.polylines(out_img, [left_curve],
                      isClosed=False, color=(0, 255, 255), thickness=3)
        cv2.polylines(out_img, [right_curve], isClosed=False,
                      color=(0, 255, 255), thickness=3)

        return out_img, left_curve, right_curve
