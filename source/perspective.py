import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

src = ((260, 720),(606, 454),(677,454),(1120,720))
dest = ((260, 720),(260, 454),(1120,454),(1120,720))

x1=(260, 720)
x2=(606, 454)
x3=(677,454)
x4=(1120,720)

img = cv2.imread('tests/perspective/snapshot.png')

plt.imshow(img)
plt.plot(x1, '.')
