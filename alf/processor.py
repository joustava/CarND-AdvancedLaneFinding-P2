import cv2
import os
import glob
from pipeline.distortion_corrector import DistortionCorrector
from pipeline.image_thresholder import ImageThresholder
from pipeline.perspective_transformer import PerspectiveTransformer
from detectors.lane_detector import LaneDetector
import numpy as np
import time
from common.roi import Roi


def create_canvas(image):
    """
    Helper returning a blank image
    """
    return np.zeros((image.shape[0], image.shape[1], 3), dtype=numpy.uint8)


def weighted_img(binary_image, original_image, α=0.75, β=1., γ=0.):
    """
    Superimpose two images
    """
    return cv2.addWeighted(original_image, α, binary_image, β, γ)


def calibrate(image_folder="./assets/camera_cal"):
    """
    Returns a calibrated DistortionCorrector object
    """
    calibration_images = []
    for filename in os.listdir(image_folder):
        img = cv2.imread(os.path.join(image_folder, filename))
        if img is not None:
            calibration_images.append(img)

    corrector = DistortionCorrector()
    corrector.calibrate(calibration_images)
    return corrector


thresholder = ImageThresholder()
warper = PerspectiveTransformer(cv2.imread('./assets/test_images/test1.jpg'))
detector = LaneDetector()


def frame_pipeline(distortion_corrector):
    def process(frame, snapshot=False):
        start = time.perf_counter()

        # 1. CALIBRATION is done once before running the pipeline.
        # 2. UNDISTORTION
        undistorted_frame = distortion_corrector.undistort(frame)

        height, width = undistorted_frame.shape[:2]

        # 3. BINARY IMAGE THRESHOLD STEP
        thresholded_frame, color_binary_frame, gradient_thresholded_frame, color_thresholded_frame = thresholder.threshold(
            undistorted_frame)

        # 4. PERSPECTIVE TRANSORMATION

        warped_image = warper.warp(thresholded_frame)

        # 5. Finding Lane Lines
        warped_lane_frame, warped_annotated_frame, left_curve, right_curve, rl, rr = detector.detect(
            warped_image)

        # 6. Unwarp image and create inset picure to visualize lane tracking
        unwarped_frame = warper.unwarp(warped_lane_frame)

        top_view_inset = cv2.resize(
            warped_annotated_frame, (0, 0), fx=0.4, fy=0.4)

        top_view_inset = cv2.copyMakeBorder(top_view_inset, 2, 2, 2, 2,
                                            cv2.BORDER_CONSTANT, value=(255, 255, 255))

        inset_h, inset_w = top_view_inset.shape[:2]
        inset_top = 10
        inset_left = 600

        cv2.rectangle(unwarped_frame, (0, 0), (width, height//2),
                      (150, 150, 150), -1)

        unwarped_frame[
            inset_top:inset_top + inset_h,
            inset_left:inset_left + inset_w] = top_view_inset
        # 7. Plot lines and radius of curvature of the lane and the position of the vehicle
        # with respect to center. We need to make and inverse transform of the lines found in 5.
        # and plot / superimpose them on the original image. The radius and vehicle center can
        # redered as text
        print((rr - rl) / 2)

        overlayed_frame = weighted_img(unwarped_frame, frame)

        text_radius1 = 'R(px): {radius}'.format(radius=rl)
        text_radius2 = 'R(m): {radius}'.format(radius=rl * 30/720)

        cv2.putText(overlayed_frame, text_radius1, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
        cv2.putText(overlayed_frame, text_radius2, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)

        # Plot camera x center
        height, width = overlayed_frame.shape[:2]
        cv2.line(overlayed_frame, (width//2, height),
                 (width//2, height-20), (30, 30, 30), 3)

        # Save examples of each step in pipeline when requested
        if snapshot:
            calibration_example = cv2.imread(
                './assets/camera_cal/calibration2.jpg')

            # Check perspective transform configuration
            # on assets/test_images/straight_lines2.jpg
            pts = np.int32(Roi.src_corners(width, height))
            src_points_frame = cv2.polylines(
                np.copy(undistorted_frame), [pts], True, (0, 0, 255), 2)
            dst_points_frame = warper.warp(src_points_frame)

            cv2.imwrite(
                './assets/output_images/undistorted_checkerboard.jpg', distortion_corrector.undistort(calibration_example))
            cv2.imwrite(
                './assets/output_images/original_frame.jpg', frame)
            cv2.imwrite(
                './assets/output_images/undistorted_frame.jpg', undistorted_frame)
            cv2.imwrite(
                './assets/output_images/gradient_thresholded_frame.jpg', gradient_thresholded_frame * 255)
            cv2.imwrite(
                './assets/output_images/color_thresholded_frame.jpg', color_thresholded_frame * 255)
            cv2.imwrite(
                './assets/output_images/color_binary_frame.jpg', color_binary_frame)
            cv2.imwrite(
                './assets/output_images/thresholded_frame.jpg', thresholded_frame)
            cv2.imwrite(
                './assets/output_images/src_points_frame.jpg', src_points_frame)
            cv2.imwrite(
                './assets/output_images/dst_points_frame.jpg', dst_points_frame)
            cv2.imwrite(
                './assets/output_images/warped_frame.jpg', warped_image)
            cv2.imwrite(
                './assets/output_images/warped_lane_frame.jpg', warped_lane_frame)
            cv2.imwrite(
                './assets/output_images/warped_annotated_frame.jpg', warped_annotated_frame)
            cv2.imwrite(
                './assets/output_images/unwarped_frame.jpg', unwarped_frame)
            cv2.imwrite(
                './assets/output_images/overlayed_frame.jpg', overlayed_frame)
            cv2.imwrite(
                './assets/output_images/inset_frame.jpg', top_view_inset)

        stop = time.perf_counter()
        print(f"Handling one frame took approx: {stop - start:0.4f} seconds")
        return overlayed_frame
    return process


def process_video():
    cap = cv2.VideoCapture("./assets/challenge/project_video.mp4")
    video_out = "./assets/output_images/project_video_result.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_out, fourcc, 20.0, (1280, 720))

    start = time.perf_counter()
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

    stop = time.perf_counter()
    print(f"Processing video took approx: {stop - start:0.4f} seconds")
    cap.release()
    out.release()
    cv2.destroyAllWindows()


pipeline = frame_pipeline(calibrate())
pipeline(cv2.imread('./assets/test_images/straight_lines2.jpg'), snapshot=True)

# process_video()
