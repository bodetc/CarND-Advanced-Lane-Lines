import numpy as np

from source.finding_lines import get_points_for_plotting
from source.observables import get_lane_size, find_lines_curvature


def check_deviation(ratio, tolerance):
    return ratio < 1. / tolerance or ratio > tolerance


def get_average_distance(fitx, line):
    if line.bestx is None:
        return 0
    diffx = np.abs(fitx - line.bestx)
    return np.average(diffx)


def check_plausibility(left_fit, right_fit, left_line, right_line):
    lane_width, off_center = get_lane_size(left_fit, right_fit)

    if lane_width > 4.5 or lane_width < 2.5:
        print('Ignoring frame due to lane width:', lane_width)
        return False

    left_curverad, right_curverad, mean_curverad = find_lines_curvature(left_fit, right_fit)

    # Only check curved roads, as the curvature radius for straight roads can be very noisy
    if mean_curverad < 900:
        if check_deviation(left_curverad / right_curverad, 1.7):
            print('Ignoring frame due to curve radius: left:', left_curverad, ' right:', right_curverad)
            return False

        if left_fit[0] * right_fit[0] < 0:
            print('Ignoring frame du to curvature being of both frame going in a different direction')
            return False

    # ploty, left_fitx, right_fitx = get_points_for_plotting(left_fit, right_fit)
    #
    # difference = get_average_distance(left_fitx, left_line)
    # if difference > 50:
    #     print('Ignoring frame due to left lane too different', difference)
    #     return False
    #
    # difference = get_average_distance(right_fitx, right_line)
    # if difference > 50:
    #     print('Ignoring frame due to right lane too different', difference)
    #     return False

    return True
