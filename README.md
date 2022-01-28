[//]: # (Image References)

[image1]: ./images/readme_images/calibration.jpeg "Original image"
[image2]: ./images/readme_images/corners.jpg "Image with corners"
[image3]: ./images/readme_images/undistorted.jpg "Undistorted image"
[image4]: ./images/readme_images/pinhole.png "Undistorted image"
[image5]: ./images/readme_images/projective.png "Example of linear perspective"
[image6]: ./images/readme_images/undistorted_vp.jpg "Undistorted image"
[image7]: ./images/readme_images/edges_vp.jpg "Edge image"
[image8]: ./images/readme_images/lines_vp.jpg "Image with lines"
[image9]: ./images/readme_images/lines.png "Illustration of line vanshing point calculation"
[image10]: ./images/readme_images/trapezoid.jpg "Image with trapezoid and vanishing point"
[image11]: ./images/readme_images/warped.jpg "Warped original image"
[image12]: ./images/readme_images/mask.jpg "Thresholded luminesence channel"
[image13]: ./images/readme_images/with_lines.jpg "Image with lanes"
[image14]: ./images/readme_images/undistorted_cf.png "Warp Example"
[image15]: ./images/readme_images/warped_cf.png "Fit Visual"
[image16]: ./images/testImages/test5.jpg "Initial image"
[image17]: ./images/readme_images/undistorted_si.jpg "Undistorted single image"
[image18]: ./images/readme_images/warped_si.jpg "Warped"
[image19]: ./images/readme_images/llab.jpg "Undistorted single image"
[image20]: ./images/readme_images/lhls.jpg "Warped"
[image21]: ./images/readme_images/blab.jpg "Initial image"
[image22]: ./images/readme_images/llab_thresh.jpg "Undistorted single image"
[image23]: ./images/readme_images/lhls_thresh.jpg "Warped"
[image24]: ./images/readme_images/blab_thresh.jpg "Initial image"
[image25]: ./images/readme_images/total_mask.jpg "Undistorted single image"
[image26]: ./images/readme_images/eroded_mask.jpg "Undistorted single image"
[image27]: ./images/readme_images/line_masks.jpg "Undistorted single image"
[image28]: ./images/readme_images/lines.jpg "Undistorted single image"
[image29]: ./images/readme_images/warped_lanes.jpg "Undistorted single image"
[image30]: ./images/outputImages/test5.jpg "Undistorted single image"

# LaneDetection - Weenend Project 2
In this project, we try to build an advanced lane detection system to augment video output with detected road lane, road-radius curvature and road-centre offset.

A clear working of the project is provided in the [*docs*](./docs) folder. To access the docs, please install [draw.io](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) plugin for Visual Studio Code by doing the following:
```
- open vs-code
- press ctrl+p
- ext install hediet.vscode-drawio
```
____________________________________________________________________
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


| Original image     | Chessboard corners | Undistorted image  |
|--------------------|--------------------|--------------------|
|![alt text][image1] |![alt text][image2] |![alt text][image3] |

The camera matrix encompases the pinhole camera model in it. It gives the relationship between the coordinates of the points relative to the camera in 3D space and position of that point on the image in pixels. If X, Y and Z are coordinates of the point in 3D space, its position on image (u and v) in pixels is calculated using: 
<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\begin{bmatrix}u\\v\\1\end{bmatrix}=s\mathbf{M}\begin{bmatrix}X\\Y\\Z\end{bmatrix}" alt="{https://latex.codecogs.com/svg.latex?\begin{bmatrix}u\\v\\1\end{bmatrix}=s\mathbf{M}\begin{bmatrix}X\\Y\\Z\end{bmatrix}}">
</p>

where **M** is camera matrix and *s* is scalar different from zero. This equation will be used later on.


| Pinhole camera model          |
|-------------------------------|
|![Pinhole camera model][image4]|
## Installation
Install all requirements by
```
pip3 install -r requirements.txt
```

### Step 2. Perspective Transform 
Next step is to find the projective transform so the original images can be warped so that it looks like the camera is placed directly above the road. OOne approach is to hand tune the source and destination points, which are required to compute the transformation matrix. On the other hand, the script that does that for us can be created based on linear perspective geometry. Let's look at the perspective geometry on the renaissance painting "Architectural Veduta" by Italian painter Francesco di Giorgio Martini. It is easy to note that all lines meet at a single point called vanishing point. The second thing to note is that the square floor tiles centered horizontally in the image, appear as trapezoids with horizontal top and bottom edges and side edges radiating from the vanishing point.  

| Architectural Veduta          |
|-------------------------------|
|![Architectural Veduta][image5]|

Our goal is to achieve exactly opposite, to transform a trapezoidal patch of the road in front of the car to a rectangular image of the road. To do so, the trapezoid needs to be defined as previously noted, horizontal top and bottom centered with respect to a vanishing point, sides radiating from the vanishing point. Of course, to define that, the first task is to find the vanishing point. 

The vanishing point is the place where all parallel lines meet, so to find it we will be using images with straight lines `straight_lines1.jpg`, `straight_lines2.jpg`. First, the images are undistorted, the Canny filter is applied and most prominent lines are identified using `cv2.HoughLinesP`. These images show how the pipeline works:

| Undistorted image  | Edges              | Image with lines   |
|--------------------|--------------------|--------------------|
|![alt text][image6] |![alt text][image7] |![alt text][image8] |

All detected lines are added to a list. The vanishing point is at the intersection of all the lines from the list. Unfortunately, when more than two lines are present, the unique intersecting point might not exist. To overcome that the vanishing point is selected as the point whose total squared distance from all the lines is minimal, thus optimization procedure will be employed. Each line found by the Hough lines can be represented by the point on it **p**<sub>i</sub> and  unit normal to it **n**<sub>i</sub>. Coordinate of the vanishing point is **vp**. So the total squared distance (and a cost function to be minimized is):
<p align="center">
<img src="https://latex.codecogs.com/svg.latex?I=\frac{1}{2}\sum\left(\mathbf{n}_i^T(\mathbf{vp}-\mathbf{p}_i)\right)^2" alt="{mathcode}">
</p>

To find the minimum the cost function is differentiated with respect to the **vp**. After some derivation the following is obtained:
<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\frac{\partial{I}}{\partial\mathbf{vp}}=0\implies\left(\sum\mathbf{n}_i\mathbf{n}_i^T\right)\mathbf{vp}=\left(\sum\mathbf{n}_i\mathbf{n}_i^T\mathbf{p}_i\right)\implies\mathbf{vp}=\left(\sum\mathbf{n}_i\mathbf{n}_i^T\right)^{-1}\left(\sum\mathbf{n}_i\mathbf{n}_i^T\mathbf{p}_i\right)" alt="{mathcode}">
</p>

Once the vanishing point is found, the top and bottom are defined manually and the trapezoid edges can be calculated. The corners of the trapezoid are used as a source points, while destination points are four corners of the new image. The size of the warped image is defined in file `settings.py`. After that, the matrix that defines the perspective transform is calculated using `cv2.getPerspectiveTransform()`. The procedure that implements the calculation of homography matrix of the perspective transform is implemented at the beginning of the python script `find_perspective_transform.py` (lines 9 - 67). Images that illustrate the procedure follow. Please note that bottom points of the trapezoid are outside of the image, what is the reason for black triangles shown in the warped image.

| Finding VP with multiple lines |Trapezoid and vanishing point|     Warped image   |
|--------------------------------|-----------------------------|--------------------|
|![alt text][image9]             |![alt text][image10]         |![alt text][image11]|

The obtained source and destination points are:

| Source        | Destination   |
|:-------------:|:-------------:|
| 375, 480      | 0, 0          |
| 905, 480      | 500, 0        |
| 1811, 685     | 500, 600      |
| -531, 685     | 0, 600        |

The selected range is quite big, but that had to be done in order to be able to find the lanes on the harder challenge video. In that video, the bends are much sharper than on the highway and might easily veer outside of the trapezoid causing the whole pipeline to fail.

Once again, lets just reflect on what is the matrix returned by the `cv2.getPerspectiveTransform()`. It tells how the perspective transformation is going to be performed and where the pixel from original image  with the coordinates (*u*, *v*) is going to move after the transformation. The destination of that pixel on the warped image would be the point with the coordinates (*u<sub>w</sub>*, *v<sub>w</sub>*). The new position is calculated using::

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\begin{bmatrix}u_w\\v_w\\1\end{bmatrix}=s\mathbf{H}\begin{bmatrix}u\\v\\1\end{bmatrix}" alt="{mathcode}">
</p>

where **H** is homography matrix returned as a result of `cv2.getPerspectiveTransform()` and *s* is scalar different from zero. 



