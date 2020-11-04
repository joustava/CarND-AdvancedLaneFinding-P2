import cv2
import glob
from pipeline.undistorter import Undistorter
from pipeline.thresholder import Thresholder
from pipeline.transformer import Transformer
from detectors.lane_detector import LaneDetector
import numpy


def create_canvas(image):
    """
    Helper returning a blank image
    """
    return numpy.zeros((image.shape[0], image.shape[1], 3), dtype=numpy.uint8)


def weighted_img(binary_image, original_image, α=0.8, β=1., γ=0.):
    """

    """
    return cv2.addWeighted(original_image, α, binary_image, β, γ)


def calibrate():
    # 1. CALIBRATION STEP

    # Get all calibration file names
    calibration_file_name = glob.glob('./assets/camera_cal/calibration*.jpg')

    # Load all calibration images
    calibration_images = list(
        map(lambda file: cv2.imread(file), calibration_file_name))

    # Create and calibrate an undistorter
    undistorter = Undistorter()
    undistorter.calibrate(calibration_images)
    return undistorter


def frame_pipeline(undistorter, snapshot=False):
    def process(frame):
        # 2. UNDISTORTION STEP
        # step2_source = cv2.imread('./assets/test_images/test5.jpg')
        undistorted_image = undistorter.undistort(frame)
        # Save example
        if snapshot:
            cv2.imwrite(
                './assets/output_images/undistorted_example.jpg', undistorted_image)

        # 3. BINARY IMAGE THRESHOLD STEP
        # step3_source = cv2.imread(
        #     './assets/output_images/undistorted_example.jpg')
        thresholder = Thresholder()
        thresholded_image = thresholder.threshold(undistorted_image)

        if snapshot:
            cv2.imwrite(
                './assets/output_images/undistorted_thresholded.jpg', thresholded_image)

        # # 4. PERSPECTIVE TRANSORMATION
        # step4_src = cv2.imread(
        #     './assets/output_images/undistorted_thresholded.jpg')
        tr = Transformer()
        warped_image, Minv = tr.warp(thresholded_image)

        if snapshot:
            cv2.imwrite(
                './assets/output_images/undistorted_warped.jpg', warped_image)

        # 5. Finding Lane Lines

        # [WIP]
        # FFS: grayscale!
        warped_image = cv2.imread(
            './assets/output_images/undistorted_warped.jpg', 0)

        # warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)

        detector = LaneDetector()
        warped_image_windowed, left_curve, right_curve = detector.fit_polynomial(
            warped_image)

        if snapshot:
            cv2.imwrite(
                './assets/output_images/undistorted_warped_windowed.jpg', warped_image_windowed)

        # 6. Plot lines and radius of curvature of the lane and the position of the vehicle
        # with respect to center. We need to make and inverse transform of the lines found in 5.
        # and plot / superimpose them on the original image. The radius and vehicle center can
        # redered as text.

        unwarped_image = cv2.warpPerspective(warped_image_windowed, Minv, (warped_image_windowed.shape[1], warped_image_windowed.shape[0]),
                                             flags=cv2.INTER_LINEAR)
        if snapshot:
            cv2.imwrite(
                './assets/output_images/undistorted_unwarped_windowed.jpg', unwarped_image)

        # original = cv2.imread('./assets/test_images/test5.jpg')

        overlayed = weighted_img(unwarped_image, frame)

        if snapshot:
            cv2.imwrite(
                './assets/output_images/overlayed.jpg', overlayed)

        return overlayed
    return process


pipeline = frame_pipeline(calibrate())
# pipeline(cv2.imread('./assets/test_images/test5.jpg'), snapshot=True)


def process_video():
    cap = cv2.VideoCapture("./assets/challenge/project_video.mp4")
    video_out = "./assets/output_images/project_video_result.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_out, fourcc, 20.0, (1280, 720))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = pipeline(frame)

            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
