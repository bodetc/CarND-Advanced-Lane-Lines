import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


src = np.float32([[260, 720],[606, 454],[677,454],[1120,720]])
dst = np.float32([[260, 720],[260, 0],[1120,0],[1120,720]])

img = mpimg.imread('snapshot.png')

M = cv2.getPerspectiveTransform(src, dst)

warped = cv2.warpPerspective(img, M, (1280,738), flags=cv2.INTER_LINEAR)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(img)
ax1.plot(260, 720, '.')
ax1.plot(606, 454, '.')
ax1.plot(677,454, '.')
ax1.plot(1120,720, '.')
ax1.set_title('Original Image', fontsize=30)

ax2.imshow(warped)
ax2.plot(260, 720, '.')
ax2.plot(260, 0, '.')
ax2.plot(1120,0, '.')
ax2.plot(1120,720, '.')
ax2.set_title('Transformed Image', fontsize=30)

plt.show()