import glob

import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

from source import util
from source.calibration import Calibration
from source.perspective import Perspective
from source.thresholds import combined_threshold

src = np.float32([[260, 685], [575, 465], [712, 465], [1050, 685]])
dst = np.float32([[260, 720], [260, 0], [1050, 0], [1050, 720]])
M = cv2.getPerspectiveTransform(src, dst)

calibration = Calibration(pickle_file='camera_cal/cam_dist_pickle.p')
perspective = Perspective()

# Make a list of test images
images = glob.glob('test_images/*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = mpimg.imread(fname)

    dst = calibration.undistort(img)
    binary = combined_threshold(dst)
    binary_warped = perspective.warpPerspective(binary)

    gray = cv2.cvtColor(binary_warped * 255, cv2.COLOR_GRAY2BGR)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    ax1.imshow(img)
    ax1.plot(260, 685, '.')
    ax1.plot(595, 450, '.')
    ax1.plot(685, 450, '.')
    ax1.plot(1050, 685, '.')
    ax1.set_title('Original Image', fontsize=30)

    ax2.imshow(gray)
    ax2.plot(320, 720, '.')
    ax2.plot(320, 0, '.')
    ax2.plot(960, 0, '.')
    ax2.plot(960, 720, '.')
    ax2.set_title('Transformed Image', fontsize=30)

    plt.savefig('tests/perspective/plot_' + util.get_filename(fname))

    mpimg.imsave('tests/perspective/' + util.get_filename(fname), gray)

    plt.show()

def wrap(img):
    dst = calibration.undistort(img)
    binary = combined_threshold(dst)
    binary_warped = perspective.warpPerspective(binary)
    gray = cv2.cvtColor(binary_warped * 255, cv2.COLOR_GRAY2BGR)
    return gray


from source.video import process_video

process_video('project_video.mp4', 'tests/perspective/project_video.mp4', wrap)
