import cv2
import os
import glob
from pipeline.distortion_corrector import DistortionCorrector
from pipeline.image_thresholder import ImageThresholder
from pipeline.perspective_transformer import PerspectiveTransformer
from detectors.lane_detector import LaneDetector
import numpy
import time


def create_canvas(image):
    """
    Helper returning a blank image
    """
    return numpy.zeros((image.shape[0], image.shape[1], 3), dtype=numpy.uint8)


def weighted_img(binary_image, original_image, α=0.75, β=1., γ=0.):
    """

    """
    return cv2.addWeighted(original_image, α, binary_image, β, γ)


def calibrate(image_folder="./assets/camera_cal"):
    """
    Returns a calibrated DistortionCorrector object
    """
    # calibration_file_name = glob.glob('./assets/camera_cal/calibration*.jpg')

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
        tic = time.perf_counter()
        # 2. UNDISTORTION STEP
        distortion_corrected_image = distortion_corrector.undistort(frame)

        # 3. BINARY IMAGE THRESHOLD STEP
        thresholded_image = thresholder.threshold(distortion_corrected_image)

        # 4. PERSPECTIVE TRANSORMATION
        warped_image = warper.warp(thresholded_image)

        # 5. Finding Lane Lines
        warped_image_windowed, left_curve, right_curve = detector.fit_polynomial(
            warped_image)

        # 6. Unwarp image
        unwarped_image = warper.unwarp(warped_image_windowed)

        # 7. Plot lines and radius of curvature of the lane and the position of the vehicle
        # with respect to center. We need to make and inverse transform of the lines found in 5.
        # and plot / superimpose them on the original image. The radius and vehicle center can
        # redered as text

        # 8. Plot results
        overlayed = weighted_img(unwarped_image, frame)

        height, width = overlayed.shape[:2]
        cv2.line(overlayed, (width//2, height),
                 (width//2, height-20), (255, 255, 0), 3)

        # Save examples
        if snapshot:
            cv2.imwrite(
                './assets/output_images/distortion_corrected_image.jpg', distortion_corrected_image)
            cv2.imwrite(
                './assets/output_images/undistorted_thresholded.jpg', thresholded_image)
            cv2.imwrite(
                './assets/output_images/undistorted_warped.jpg', warped_image)
            cv2.imwrite(
                './assets/output_images/undistorted_warped_windowed.jpg', warped_image_windowed)
            cv2.imwrite(
                './assets/output_images/undistorted_unwarped_windowed.jpg', unwarped_image)
            cv2.imwrite(
                './assets/output_images/overlayed.jpg', overlayed)

        toc = time.perf_counter()
        print(f"Handling one frame took approx: {toc - tic:0.4f} seconds")
        return overlayed
    return process


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


pipeline = frame_pipeline(calibrate())
pipeline(cv2.imread('./assets/test_images/test1.jpg'), snapshot=True)
