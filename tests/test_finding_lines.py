import glob

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from source.calibration import Calibration
from source.finding_lines import find_lines, refit_line, plot_lane
from source.observables import print_observables
from source.perspective import Perspective
from source.thresholds import combined_threshold

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

    left_fit, right_fit = find_lines(binary_warped, plot=True)

    left_fit, right_fit = refit_line(binary_warped, left_fit, right_fit, plot=False)

    print_observables(left_fit, right_fit)

    final = plot_lane(dst, binary_warped, perspective, left_fit, right_fit)

    plt.imshow(final)

    plt.show()


def process_image(img):
    dst = calibration.undistort(img)
    image = perspective.warpPerspective(dst)
    binary_warped = combined_threshold(image)

    left_fit, right_fit = find_lines(binary_warped)

    return plot_lane(dst, binary_warped, perspective, left_fit, right_fit)


from source.video import process_video

process_video('project_video.mp4', 'tests/finding_lines/project_video.mp4', process_image)
