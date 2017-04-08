import glob

import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

from source import util
from source.calibration import Calibration
from source.thresholds import combined_threshold

calibration = Calibration(pickle_file='camera_cal/cam_dist_pickle.p')

# Make a list of test images
images = glob.glob('test_images/*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = mpimg.imread(fname)

    dst = calibration.undistort(img)
    final = combined_threshold(dst)

    # Plot the result
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    ax1.imshow(img)
    ax1.set_title('Original Image', fontsize=50)
    ax2.imshow(final, cmap='gray')
    ax2.set_title('Thresholded Gradient', fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

    plt.show()

    mpimg.imsave('output_images/thresholds/' + util.get_filename(fname), cv2.cvtColor(final * 255, cv2.COLOR_GRAY2BGR))

from source.video import process_video


def process_image(img):
    binary = combined_threshold(img)
    out_img = np.dstack((binary, binary, binary)) * 254
    return np.asarray(out_img, dtype=np.dtype(np.uint8))


process_video('project_video.mp4', 'output_videos/thresholds/project_video.mp4', process_image)
