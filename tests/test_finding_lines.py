import glob

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from source import util
from source.calibration import Calibration
from source.finding_lines import find_lines, refit_line, plot_lane, add_caption
from source.observables import print_observables, find_lines_curvature, get_lane_size
from source.perspective import Perspective
from source.thresholds import combined_threshold
from source.video import process_video

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

    left_fit, right_fit = find_lines(binary_warped, plot=True,
                                     filename='output_images/finding_lines/plot_' + util.get_filename(fname))

    left_fit, right_fit = refit_line(binary_warped, left_fit, right_fit, plot=True,
                                     filename='output_images/finding_lines/plot_refit_' + util.get_filename(fname))

    print_observables(left_fit, right_fit)

    lane_width, off_center = get_lane_size(left_fit, right_fit)
    left_curverad, right_curverad, mean_curverad = find_lines_curvature(left_fit, right_fit)

    final = plot_lane(dst, binary_warped, perspective, left_fit, right_fit)
    final = add_caption(final, mean_curverad, off_center)

    plt.imshow(final)

    mpimg.imsave('output_images/finding_lines/' + util.get_filename(fname), final)

    plt.show()


def process_image(img):
    dst = calibration.undistort(img)
    image = perspective.warpPerspective(dst)
    binary_warped = combined_threshold(image)

    left_fit, right_fit = find_lines(binary_warped)

    return plot_lane(dst, binary_warped, perspective, left_fit, right_fit)

# process_video('project_video.mp4', 'output_videos/finding_lines/project_video.mp4', process_image)
