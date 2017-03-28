import numpy as np
import cv2
import pickle


class Calibration:
    """A class for transforming the """
    mtx = None
    dist = None

    def __init__(self, images=None, pickle_file=None):
        self.mtx = []
        self.dist = []

        if images is None and pickle_file is None:
            raise Exception("Please provide either image glob or pickle file!")

        if images is not None:
            self.calibrate_camera(images)

        if pickle_file is not None:
            self.from_pickle(pickle_file)

    def calibrate_camera(self, images):
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6 * 9, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d points in real world space
        imgpoints = []  # 2d points in image plane.

        # Step through the list and search for chessboard corners
        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            # If found, add object points, image points
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)
            else:
                print("No corners found for image ", fname)

        img_size = (1280, 720)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
        self.mtx = mtx
        self.dist = dist

    def from_pickle(self, pickle_file):
        dist_pickle = pickle.load(open(pickle_file, "rb"))
        self.mtx = dist_pickle["mtx"]
        self.dist = dist_pickle["dist"]

    def save_pickle(self, pickle_file):
        dist_pickle = {}
        dist_pickle["mtx"] = self.mtx
        dist_pickle["dist"] = self.dist
        pickle.dump(dist_pickle, open(pickle_file, "wb"))

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
