import cv2
import numpy as np

class Perspective:
    """A class for performing perspective transformation on the lane lines"""

    M = None

    def __init__(self, src = np.float32([[260, 685], [575, 465], [712, 465], [1050, 685]]),
        dst = np.float32([[260, 720], [260, 0], [1050, 0], [1050, 720]])):

        self.M = cv2.getPerspectiveTransform(src, dst)

    def warpPerspective(self, image):
        return cv2.warpPerspective(image, self.M, (1280, 720), flags=cv2.INTER_LINEAR)