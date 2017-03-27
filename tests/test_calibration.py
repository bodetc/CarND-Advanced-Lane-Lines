import glob
import cv2
import matplotlib.pyplot as plt

from source import calibration

# Make a list of calibration images
images = glob.glob('camera_cal/calibration*.jpg')

mtx, dist = calibration.calibrate_camera(images)

img = cv2.imread('camera_cal/calibration1.jpg')
dst = calibration.undistort(img, mtx, dist)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=30)
ax2.imshow(dst)
ax2.set_title('Undistorted Image', fontsize=30)

plt.show()

from source.video import process_video

process_video('project_video.mp4', 'tests/calibration/project_video.mp4',
              lambda image: calibration.undistort(image, mtx, dist))
