import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2
import os
import pickle
import utilities as ut
from utilities import Arrow3D
import QRCode 
from settings import *



def camPoseEstimate(image):
    size = image.shape
    pattern_points = np.array(QRCode.detectQRcode(image),dtype="double")
    model_points = np.array([
        (-QRCodeSide/2,QRCodeSide/2,0.0),
        (QRCodeSide/2,QRCodeSide/2,0.0),
        (QRCodeSide / 2, -QRCodeSide / 2, 0.0), 
        (-QRCodeSide / 2, -QRCodeSide / 2, 0.0) 
    ])
    if not os.path.exists('./calibration.pckl'):
        print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
        exit()
    else:
        f = open('calibration.pckl', 'rb')
        (camera_intrinsic_matrix, dist_coeffs) = pickle.load(f)   
        f.close()
        if camera_intrinsic_matrix is None or dist_coeffs is None:
            print("Calibration issue. Remove ./calibration.pckl and recalibrate your camera with CalibrateCamera.py.")
            exit()
    flag, rotation_vector,translation_vector = cv2.solvePnP(
        model_points,
        pattern_points,
        camera_intrinsic_matrix,
        dist_coeffs,
        flags = cv2.SOLVEPNP_ITERATIVE
    )
    rotation_matrix, jacobian = cv2.Rodrigues(rotation_vector)
    camera_pose = np.matmul(-rotation_matrix.transpose(),translation_vector)
    return camera_pose
    