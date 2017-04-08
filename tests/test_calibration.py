import glob

import cv2
import matplotlib.pyplot as plt

from source import util
from source.calibration import Calibration

# Make a list of calibration images
images = glob.glob('camera_cal/calibration*.jpg')

calibration = Calibration(images=images)
calibration.save_pickle('camera_cal/cam_dist_pickle.p')


def test_calibration(images):
    # Step through the list and search for chessboard corners
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        dst = calibration.undistort(img)

        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        ax2.set_title('Undistorted Image', fontsize=30)

        plt.show()
        cv2.imwrite('output_images/calibration/' + util.get_filename(fname), dst)


test_calibration(images)

# Undistort the test images
images = glob.glob('test_images/*.jpg')
test_calibration(images)

from source.video import process_video

process_video('project_video.mp4', 'output_videos/calibration/project_video.mp4', calibration.undistort)
