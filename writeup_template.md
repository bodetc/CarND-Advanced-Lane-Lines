#Advanced Lane Finding Project

In this project, I will create a pipeline to identify the lane boundaries in a video of a car driving on the highway.
Numerical observables such as lane curvature and the position of the vehicle within the lane are alos calculated.

First, the camera is calibrated by computing the camera calibration matrix and distortion coefficients.
This is done using the given chessboard calibration images.
Then, a picture pipeline is implemented to process the provided test images.

The pipeline contains the following steps:

* Distortion correction of the camera image,
* Creation of a thresholded binary image,
* Applying a perspective transform to create a bird's eye view,
* Implementation of a lane finding algorithm
* Determination of the lane curvature and vehicle position within the lane,
* Plotting the resulting lanes boundaries and numerical observables back into the original image.

Finally, the developed picture pipeline is transformed into a video pipeline and applied to the provided project video.

This project can also be found on [GitHub](https://github.com/bodetc/CarND-Advanced-Lane-Lines).

[//]: # (Image References)

[original_calibration]: ./camera_cal/calibration4.jpg "Original"
[undistorted_calibration]: ./output_images/calibration/calibration4.jpg "Undistorted"
[original]: ./test_images/test2.jpg "Original"
[undistorted]: ./output_images/calibration/test2.jpg "Undistorted"
[thresholds]: ./output_images/thresholds/test2.jpg "Undistorted"
[perspective_plot]: ./output_images/perspective/plot_straight_lines1.jpg "Undistorted"
[perspective]: ./output_images/perspective/test2.jpg "Undistorted"
[finding_lanes1]: ./output_images/finding_lines/plot_test2.jpg "Undistorted"
[finding_lanes2]: ./output_images/finding_lines/plot_refit_test2.jpg "Undistorted"
[final]: ./output_images/finding_lines/test2.jpg "Undistorted"
[polynomial]: ./polynomial.png "Polynomial"
[curvature]: ./curvature.png "Cuvature"
[video1]: ./project_video.mp4 "Video"

##Camera Calibration

The first step in the pipeline was to correct the input images for camera distortion.
This was done by calculating the camera calibration matrix and distortion coefficient using the provided calibration images.
The code for fitting the calibration and applying the camera calibration is contained in `source/calibration.py`
The code the performing calibration is contained in the method `calibrate_camera`.

I used the functionality provided by OpenCV to calculate the camera matrix and distortion coefficients using the calibration chessboard images provided in the repository.
The first step was to create `objpoints` and `imgpoints` based on images of checkboards using the `cv2.findChessboardCorners()` function.
I then used this output to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.

The distortion correction is applied by using the `undistort` in the `Calibration`class.
This method uses `cv2.undistort()` to undistort the images using the calibration and distortion coefficients calculated above

Using `undistort` to undistort a sample calibration image yields the following result (first orginal, then undistorted output):
![alt text][original_calibration]
![alt text][undistorted_calibration]

##Pipeline (single images)

In this section, I will discussed the pipeline used to add the lane lines on single images.
The following original unprocessed image will be used as an example thorough the pipeline:
![alt text][original]

### Distortion correction

The first step, distortion correction, is applied by using the `undistort` method discussed in the previous section.
Once undistorted, the example image looks like this:
![alt text][undistorted]

### Creation of a thresholded binary image

The code for generating thresholded binary images is located in `source/thresholds.py`
The code for performing the transformation on the test images is in `tests/test_thresholds.py`.

* A color selection threshold `color` that selects colors using hard coded thresholds in the HLS space.
This threshold selection is presented [here](https://medium.com/towards-data-science/robust-lane-finding-using-advanced-computer-vision-techniques-mid-project-update-540387e95ed3)
and was suggested as reading material by the first reviewer of the this project.
The first step is to transform the image into HLS space
This allows for a more robust detection with different brightness condition as the luminance is stored in a separate channel.
Then, the lines are selected using two binary threshold filters.
The yellow filter will select pixel with HLS values between `[0, 80, 200]` and `[40, 255, 255]`.
The white filter will select pixel with HLS values between `[20, 0, 200]` and `[255, 80, 255]`.
* A binary threshold `gradx` for the X-gradient with values between 20 and 100.
* A S-channel `hls_binary` threshold with values between 170 and 255.
This threshold first convert the image to HLS before performing a binary selection on the S channel.
* A direction threshold gradient `dir_binary` that select pixels where the gradient direction is between 0.9 and 1.3 radians.

Those thresholds are combined in the following way:
`(color == 1) | (((gradx == 1) | (hls_binary == 1)) & (dir_binary == 1))`
After manual testing on problematic frames of the videos (see `test_images\vlcsnap-*`)
this combination seem to be providing the best solution in most conditions,
including under shadows and with bright concrete.

Finally, in order to remove some of the noise that was still selected through the thresholding, erosion is applied to the combined image.
The [OpenCV function](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html)
is used with a kernel of 11x11 to remove the noisy patches.
This method was suggested in [this blog](https://medium.com/@ajsmilutin/advanced-lane-finding-5d0be4072514)
that covers the same project and that was suggested by the first reviewer.

Here is the sample image after applying thresholding
![alt text][thresholds]

### Perspective transformation

The code for my perspective transform is located in `source/perspective.py` in a `Perspective` class.
The class can be created by providing source and destination points. 
If it is not the case, the the following source and destination points will be used by default:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 595, 450      | 320, 0        | 
| 260, 685      | 320, 720      |
| 1050, 685     | 960, 720      |
| 685, 450      | 960, 0        |

I verified that my perspective transform was working as expected and that the default value for the source and destination points were correct 
by drawing those points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image, when taking a straight line as input.
![alt text][perspective_plot]

Furthermore, here is the result of perspective transformation on the test image:
![alt text][perspective]

### Lane line identification

Two methods were used for finding lane lines on the wrapped binary image.
The code for both methods can be found in the file `finding_lines.py`.
The first method searches for line lanes without prior knowledge, and is implemented in the `find_lines` function.
It starts by build and histogram of the lower half of the image
then finds the largest peaks in each of the left and right halves of the images.
Those peaks will be the starting point for the left and right lanes.

The first and last 160 pixels of the image are ignored it this step,
as they are too far off-center from the camera (around 3-4 meters)
and tend to contain large peaks related to the scenery at the side of the road.

Afterwards, a sliding window method is used to find the relevant lane points.
The image is first divided vertically into 9 slides.
Then, for each window starting in the bottom, all the points in the window are selected, then the next window is recentered on _center of mass_ of the selected points of the current window.
This recentering occurs only if enough points were detected in the current window.

Finally, a polynomial fit is performed on all the selected points for each of the two lanes.
The resulting windows (in green), selected points (in red and blue) as well as the resulting polynomial fit can be seen below for the sample image:

![alt text][finding_lanes1]

The second method assumes that the approximate location of the lane is already known,
for instance from a previous frame. Therefore, it will only be used in the video pipeline below.
This method is implemented in the `refit_line` function.

In this method, the search windows are defined by searching in a certain margin around the previous fit.
All the point in the two search windows are selected, and a new fit is performed on those points.
An example of this method can be seen below:
![alt text][finding_lanes2]

### Observables calculation
The radius of curvature of the lane can be calculated from the polynomial that was used in the lane line fitting.
The radius is given by the following equation:

![alt text][curvature]

where our polynomial has the form
![alt text][polynomial].

If we use this equation as is with the polynomial calculated in the previous section, the resulting number will not be in meters, but in some combinations of pixel size in the x and y direction.

To provide proper scaling, assumptions were made on the image used for tuning the perspective transformation (`straight_line_1.jpg`).
First, we assume that the lane has a width of 3.7 m. As this is transformed into a width of 640 pixels, this give a scaling of around 6 cm per pixel in the x direction.
Secondly, the dashed lane are assumed to have a length of 3 m. As they are measured at around 80 pixels in the warped image, this gives a scaling of around 4 cm per pixel in the y direction.

The coefficients `A` and `B`, as well as the values of `x` and `y` must be rescaled appropriately when calculating the radius using the equation above.

To find the distance to the center of lane, the position of the left and right lane at the bottom of the image is calculated from the fit.
Then the center position of the lane (in pixel) is calculated, and the distance to the center of the image is taken and converted to physical units.

The code for calculating those observables can be found in the file `source/observables.py`

For the test image used so far, the radius of curvature is calculated at 272 m and the vehicle is currently 28 cm left of the center of lane.

### Plotting

The lane lines were plotted as a polygon in the top-down perspective, then transformed back using the reverse perspective transformation.
The resulting polygon is added with transparency to the undistorted image
The code for this can be found in the function `plot_lane` in `finding_lanes.py`.

As a final step, the calculated radius and distance from center is also added to the image, see `add_caption` in `finding_lanes.py`.

The final result on the sample image can be seen here:
![alt text][final]

##Pipeline (video)

The video pipeline simply process all frames of the video one by one using the picture pipeline.
The differences are that a sanity check is performed on the output and that the lane lines are not searched on the full picture (see discussion above).

The plausibility check is implemented in the method `check_plausibility` of `source\plausibility.py`.
The first check ensure that the lane width has plausible values (between 2.5 and 4.5 meters).
The second check ensure that the the two lane lines have similar curvature, i.e. that the ratio of their curvature is included between 1/1.7 and 1.7.
This check is only performed if the road has a curvature under 700 meters, as the curvature measurement for straight lines is unstable.
In that case, it is also checked that the curvature of both lane lines is in the same direction.

The video pipeline can be found in `source\advanced_lane_finding.py`
Here's a [link to my video result](./output_videos/project_video.mp4)

##Discussion

The final video properly manages to follow the lane lines most of the time. The lanes are still wobbly at the transitions between different concrete colors, or between light and shadows.
It was difficult to choose the proper values for the threshold, in a way that works for all images.

Some solutions might be to renormalize the image for luminosity, as was done in previous project. On could also dynamically change the thresholds used in the creation of the binary image, it order to be able to handle more scenario.

Another idea might be to take the average color in the perspective transformed image (which should contain mostly concrete, whichever color it has), and look in an image that contains only the difference to that average.

This pipeline is also likely to fail in poor weather condition, or when the road is wet and sun reflections prevents the camera form properly seeing the lines.
Furthermore, the lane lines could be masked by snow or leaves and prevent this algorithm form working properly.
Also, in dense traffic, they might not be enough distance to the preceding car to have a long enough clear view to properly fit the lane lines.

In Germany, lanes overriden within road works by adding yellow lines to the roads, the existing white lines are not removed but must be ignore. This case would not at all be supported by the current version of the pipeline.

##Remark

In order to be complete, and avoid any claims of plagiarism, 
I was encountering the same _black plot_ problem as in [this StackOverflow question](http://stackoverflow.com/questions/42044259/getting-black-plots-with-plt-imshow-after-multiplying-image-array-by-a-scalar).
I solved the problem by converting the arrays to uint8 as suggested.
It is clear from the screenshots that this question relates to the current project, I prefer to mention that I saw this post and used the result.
I must say however that this question mainly concerns a technical aspect of the project.