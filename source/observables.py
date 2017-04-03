import numpy as np

# Define conversions in x and y from pixels space to meters
ym_per_pix = 3. / 80.  # meters per pixel in y dimension
xm_per_pix = 3.7 / 640.  # meters per pixel in x dimension

# Define y-value where we want radius of curvature
# I'll choose the maximum y-value, corresponding to the bottom of the image
y_eval = 720
y_eval_rs = y_eval * ym_per_pix


def get_radius_of_curvature(fit):
    A_rs = fit[0] * xm_per_pix / ym_per_pix ** 2
    B_rs = fit[1] * xm_per_pix / ym_per_pix

    curverad = ((1 + (2 * A_rs * y_eval_rs + B_rs) ** 2) ** 1.5) / np.absolute(2 * A_rs)

    return curverad


def find_lines_curvature(left_fit, right_fit):
    left_curverad = get_radius_of_curvature(left_fit)
    right_curverad = get_radius_of_curvature(right_fit)
    mean_curverad = np.sqrt(left_curverad * right_curverad)
    return left_curverad, right_curverad, mean_curverad


def get_line_base_position(fit):
    x = np.polyval(fit, y_eval)
    return (x - 640) * xm_per_pix


def get_lane_size(left_fit, right_fit):
    left_x = get_line_base_position(left_fit)
    right_x = get_line_base_position(right_fit)

    lane_width = right_x - left_x
    off_center = (left_x + right_x) / 2

    return lane_width, off_center


def print_observables(left_fit, right_fit):
    left_curverad, right_curverad, mean_curverad = find_lines_curvature(left_fit, right_fit)
    print('Curvature:', mean_curverad, 'm, left-right ratio:', left_curverad/right_curverad)
    lane_width, off_center = get_lane_size(left_fit, right_fit)
    print('Width:', lane_width, 'm, off-center', off_center, 'm')
