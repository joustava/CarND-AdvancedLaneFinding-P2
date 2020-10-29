import cv2
import glob
from pipeline.undistorter import Undistorter
from pipeline.thresholder import Thresholder
from detectors.corner_detector import CornerDetector


def example():
    # 1. CALIBRATION STEP

    # Get all calibration file names
    calibration_file_name = glob.glob('./assets/camera_cal/calibration*.jpg')

    # Load all calibration images
    calibration_images = list(
        map(lambda file: cv2.imread(file), calibration_file_name))

    # Create and calibrate an undistorter
    undistorter = Undistorter()
    undistorter.calibrate(calibration_images)

    # 2. UNDISTORTION STEP
    step2_source = cv2.imread('./assets/test_images/test5.jpg')
    step2_dst = undistorter.undistort(step2_source)
    # Save example
    cv2.imwrite(
        './assets/output_images/test5_undistorted_example.jpg', step2_dst)

    # 3. BINARY IMAGE THRESHOLD STEP
    step3_source = cv2.imread(
        './assets/output_images/test5_undistorted_example.jpg')
    thresholder = Thresholder()
    step3_dst = thresholder.threshold(step3_source)
    cv2.imwrite(
        './assets/output_images/test5_undistorted_thresholded.jpg', step3_dst)

    # 4. PERSPECTIVE TRANSORMATION
    step4_src = cv2.imread(
        './assets/output_images/test5_undistorted_thresholded.jpg')
    print(step4_src)
    detector = CornerDetector()
    corners = detector.find(step4_src)
    cv2.imwrite('./assets/output_images/corners_example.jpg', corners)


example()
