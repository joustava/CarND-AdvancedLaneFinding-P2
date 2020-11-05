import numpy as np
import cv2


class DistortionCorrector(object):
    """
    Removes lens distortion from images.

    Before undistorting an image with `undistort()` an Undistorter object needs to be calibrated
    with the help of a set of checkerboard images passed to `calibrate()`. These images need to be created
    with the same camera and lens combination as the actual images you'd like to process.
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
        height = image.shape[0]
        width = image.shape[1]
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self._object_points, self._image_points, (height, width), None, None)
        return cv2.undistort(image, mtx, dist, None, mtx)
