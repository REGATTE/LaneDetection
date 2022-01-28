# LaneDetection - Weenend Project 2
In this project, we try to build an advanced lane detection system to augment video output with detected road lane, road-radius curvature and road-centre offset.

A clear working of the project is provided in the [*docs*]() folder. To access the docs, please install [draw.io]() plugin for Visual Studio Code by doing the following:

### Step 1. Callibrate Camera
Camera Calibration Image distortion occurs when cameras look at objects that have 3D features in the real world and want to transform them into 2D planes in the image. This transformation is not efficient and would bring a lot of distortion to the picture. This distortion changes the shape and size of the object in this transformation. So, the first step in analyzing the image distortion level is the pre-processing step. 

This step has a significant effect on the performance of lane detection because distorted images show the lane of the image in some parts curvy, keep out the detection application from reality and make an image look tilted so that some objects appear farther away or closer than they are in fact. Camera Calibration maps 3D points 2D points one. This can be done with images with grid patterns such as a chessboard. This process uses multiple photos of chessboards from different distances and angles. The images are put as input and return the camera calibration values. We use this value matrix with the original images of datasets to make them unsorted images. 

Steps: 
- undistort the images coming from camera, thus improving the quality of geometrical measurement.
- estimate the spatial resolution of pixels per meter in both x and y directions

For this project, the calibration pipeline is implemented in function **`calibrate`** implemented in file `calibrate.py`. The procedure follows these steps:

- The procedures start by preparing "object points", which will be the `(x, y, z)` coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0. Also, I am assuming that the size of the chessboard pattern is the same for all images, so the object points will be the same for each calibration image.

- Then, the calibration images are sequentially loaded, converted to grayscale and chessboard pattern is looked for using `cv2.findChessboardCorners`. When the pattern is found, the positions of the corners get refined further to sub-pixel accuracy using `cv2.cornerSubPix`. That improves the accuracy of the calibration. Corner coordinates get appended to the list containing all the image points, while prepared "object points" gets appended to the list containing all the object points.

- The distortion coefficients and camera matrix are computed using `cv2.calibrateCamera()` function, where image and object points are passed as inputs. It is important to check if the result is satisfactory, since calibration is a nonlinear numerical procedure, so it might yield suboptimal results. To do so calibration images are read once again and undistortion is applied to them. The undistorted images are shown in order to visually check if the distortion has been corrected. Once the data has been checked the parameters are is pickled saved to file. One sample of the input image, image with chessboard corners and the undistorted image is shown:

[//]: # (Image References)

[image1]: ./readme_images/calibration.jpeg "Original image"
[image2]: ./readme_images/corners.jpg "Image with corners"
[image3]: ./readme_images/undistorted.jpg "Undistorted image"

| Original image     | Chessboard corners | Undistorted image  |
|--------------------|--------------------|--------------------|
|![alt text][image1] |![alt text][image2] |![alt text][image3] |

The camera matrix encompases the pinhole camera model in it. It gives the relationship between the coordinates of the points relative to the camera in 3D space and position of that point on the image in pixels. If X, Y and Z are coordinates of the point in 3D space, its position on image (u and v) in pixels is calculated using: 
<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\begin{bmatrix}u\\v\\1\end{bmatrix}=s\mathbf{M}\begin{bmatrix}X\\Y\\Z\end{bmatrix}" alt="{https://latex.codecogs.com/svg.latex?\begin{bmatrix}u\\v\\1\end{bmatrix}=s\mathbf{M}\begin{bmatrix}X\\Y\\Z\end{bmatrix}}">
</p>

where **M** is camera matrix and *s* is scalar different from zero. This equation will be used later on.

[image4]: ./readme_images/pinhole.png "Undistorted image"

| Pinhole camera model          |
|-------------------------------|
|![Pinhole camera model][image4]|
## Installation
Install all requirements by
```
pip3 install -r requirements.txt
```