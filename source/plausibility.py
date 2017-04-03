from source.observables import get_lane_size, find_lines_curvature


def check_plausibility(left_fit, right_fit):
    lane_width, off_center = get_lane_size(left_fit, right_fit)

    if lane_width > 4.5 or lane_width < 2.5:
        print('Ignoring frame due to lane width:', lane_width)
        return False

    left_curverad, right_curverad, mean_curverad = find_lines_curvature(left_fit, right_fit)

    # Only check curved roads, as the curvature radius for straight roads can be very noisy
    if mean_curverad < 700:
        ratio = left_curverad / right_curverad
        if ratio < 1 / 1.7 or ratio > 1.7:
            print('Ignoring frame due to curve radius: left:', left_curverad, ' right:', right_curverad)
            return False

    # ploty, left_fitx, right_fitx = get_points_for_plotting(left_fit, right_fit)

    return True
