import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from source.thresholds import combined_threshold

from source.calibration import Calibration

src = np.float32([[260, 685], [575, 465], [712, 465], [1050, 685]])
dst = np.float32([[260, 720], [260, 0], [1050, 0], [1050, 720]])
M = cv2.getPerspectiveTransform(src, dst)

calibration = Calibration(pickle_file='camera_cal/cam_dist_pickle.p')

# Make a list of test images
images = glob.glob('test_images/*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = mpimg.imread(fname)

    dst = calibration.undistort(img)
    image = cv2.warpPerspective(dst, M, (1280, 720), flags=cv2.INTER_LINEAR)
    final = combined_threshold(image)

    # Plot the result
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    ax1.imshow(img)
    ax1.set_title('Original Image', fontsize=50)
    ax2.imshow(final, cmap='gray')
    ax2.set_title('Thresholded Gradient', fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

    plt.show()
