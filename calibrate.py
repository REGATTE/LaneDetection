import cv2
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pickle
from settings import CALIB_FILE_NAME, imagesPath

def calibrate(filename, silent = True):
    cam_x = 9
    cam_y = 6

    objp = np.zeros((cam_y*cam_x, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cam_x, 0:cam_y].T.reshape(-1, 2)
    image_points = []
    obj_dot = []

    term_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


    for image_file in os.listdir(imagesPath):
        if image_file.endswith("jpg"):
          
            img = mpimg.imread(os.path.join(imagesPath, image_file))
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            found, corners = cv2.findChessboardCorners(img_gray, (cam_x, cam_y))


    
    ret, matrix, distance, rvecs, tvecs = cv2.calibrateCamera(obj_dot, image_points, img_gray.shape[::-1], None, None)
    img_size  = img.shape
    calib_data = {'cam_matrix':matrix,
                  'dist_coeffs':distance,
                  'img_size':img_size}
    with open(filename, 'wb') as f:
        pickle.dump(calib_data, f)

    if not silent:
        for image_file in os.listdir(imagesPath):
            if image_file.endswith("jpg"):
              
                img = mpimg.imread(os.path.join(imagesPath, image_file))
                plt.imshow(cv2.undistort(img, matrix, distance))
                plt.show()

    return matrix, distance

if __name__ == '__main__':
    calibrate(CALIB_FILE_NAME, True)
