import numpy as np

from source.calibration import Calibration
from source.finding_lines import find_lines, plot_lane, refit_line
from source.observables import get_line_base_position, get_radius_of_curvature
from source.perspective import Perspective
from source.plausibility import check_plausibility
from source.thresholds import combined_threshold

ploty = np.linspace(0, 719, 720)


# Define a class to receive the characteristics of each line detection
class Line():
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False
        # number of iterations since the lase detection
        self.last_detected = 0
        # average x values of the fitted line over the last n iterations
        self.bestx = None
        # polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        # radius of curvature of the line in some units
        self.radius_of_curvature = None
        # distance in meters of vehicle center from the line
        self.line_base_pos = None

    def update_fit(self, fit):
        self.do_update_fit(fit)

    def do_update_fit(self, fit):
        self.detected = True
        self.last_detected = 0

        self.current_fit = fit
        self.radius_of_curvature = get_radius_of_curvature(fit)
        self.line_base_pos = get_line_base_position(fit)

        # if self.best_fit is not None:
        #    self.best_fit = .5 * fit + .5 * self.best_fit
        # else:
        self.best_fit = fit

        self.bestx = self.best_fit[0] * ploty ** 2 + self.best_fit[1] * ploty + self.best_fit[2]

    def do_not_update_fit(self):
        self.detected = False
        self.last_detected += 1


left_line = Line()
right_line = Line()

calibration = Calibration(pickle_file='camera_cal/cam_dist_pickle.p')
perspective = Perspective()


def process_image(img):
    dst = calibration.undistort(img)
    image = perspective.warpPerspective(dst)
    binary_warped = combined_threshold(image)

    if left_line.best_fit is None or right_line.best_fit is None\
            or left_line.last_detected > 5 or right_line.last_detected > 5:
        print('Searching for lane on full image')
        left_fit, right_fit = find_lines(binary_warped)
    else:
        left_fit, right_fit = refit_line(binary_warped, left_line.best_fit, right_line.best_fit)

    if check_plausibility(left_fit, right_fit):
        left_line.update_fit(left_fit)
        right_line.update_fit(right_fit)
    else:
        left_line.do_not_update_fit()
        right_line.do_not_update_fit()

    return plot_lane(dst, binary_warped, perspective, left_line.best_fit, right_line.best_fit)


from source.video import process_video

process_video('project_video.mp4', 'tests/project_video.mp4', process_image)
