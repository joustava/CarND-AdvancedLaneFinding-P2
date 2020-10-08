import glob
import os
import numpy as np
import cv2


class Undistorter(object):
    """
    Removes lens distortion from images.

    Before undistorting an image with `undistort()` an Undistorter object needs to be calibrated
    with the help of a set of checkerboard images passed to `calibrate()`. These images need to be created
    with the same camera and lens combination. 
    """

    def __init__(self, nx=9, ny=6):
        self._nx = nx
        self._ny = ny
        self._image_points = []
        self._object_points = []
        objs = np.zeros((ny*nx, 3), np.float32)
        objs[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
        self._objs = objs

    def calibrate(self, images):
        """
        Calibrates the undistorter based on the passed images.
        """

        for idx, image in enumerate(images):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, (self._nx, self._ny), None)

            # If found, draw corners
            if ret == True:
                self._image_points.append(corners)
                self._object_points.append(self._objs)
                # Draw and the corners and save file
                # cv2.drawChessboardCorners(
                #     image, (self._nx, self._ny), corners, ret)

                # cv2.imwrite(
                #     './assets/output_images/chessboard%s.jpg' % idx, image)

    def undistort(self, image):
        """
        Removes the distortion from images made with the same camera and lens combination used in the
        calibration step.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self._object_points, self._image_points, gray.shape[::-1], None, None)
        return cv2.undistort(image, mtx, dist, None, mtx)


#
if __name__ == "__main__":
    files = glob.glob('./assets/camera_cal/calibration*.jpg')
    images = list(map(lambda file: cv2.imread(file), files))
    cal = Undistorter()
    cal.calibrate(images)
    test = cv2.imread('./assets/test_images/test1.jpg')
    dst = cal.undistort(test)
    cv2.imwrite('./assets/output_images/test1_undistorted_example.jpg', dst)
