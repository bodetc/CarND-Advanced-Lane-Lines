import glob
import cv2
import matplotlib.pyplot as plt

from source.calibration import Calibration

# Make a list of calibration images
images = glob.glob('camera_cal/calibration*.jpg')

calibration = Calibration(images=images)
calibration.save_pickle('camera_cal/cam_dist_pickle.p')

img = cv2.imread('camera_cal/calibration1.jpg')
dst = calibration.undistort(img)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=30)
ax2.imshow(dst)
ax2.set_title('Undistorted Image', fontsize=30)

plt.show()

img = cv2.imread('tests/snapshot.png')
dst = calibration.undistort(img)
cv2.imwrite('tests/calibration/snapshot.png', dst)

from source.video import process_video

process_video('project_video.mp4', 'tests/calibration/project_video.mp4', calibration.undistort)
