import glob

import matplotlib.image as mpimg

from source.calibration import Calibration
from source.perspective import Perspective
from source.thresholds import combined_threshold
from source.finding_lines import find_lines

calibration = Calibration(pickle_file='camera_cal/cam_dist_pickle.p')
perspective = Perspective()

# Make a list of test images
images = glob.glob('test_images/*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = mpimg.imread(fname)

    dst = calibration.undistort(img)
    image = perspective.warpPerspective(dst)
    binary_warped = combined_threshold(image)

    out_img = find_lines(binary_warped, plot=True)

    # # Plot the result
    # f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    # f.tight_layout()
    # ax1.imshow(img)
    # ax1.set_title('Original Image', fontsize=50)
    # ax2.imshow(binary_warped, cmap='gray')
    # ax2.set_title('Thresholded Gradient', fontsize=50)
    # plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    #
    # plt.show()


def process_image(img):
    dst = calibration.undistort(img)
    image = perspective.warpPerspective(dst)
    binary_warped = combined_threshold(image)

    return find_lines(binary_warped)


from source.video import process_video

# process_video('project_video.mp4', 'tests/finding_lines/project_video.mp4', process_image)
