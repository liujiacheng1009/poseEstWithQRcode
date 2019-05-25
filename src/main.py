import datetime
import imutils
import time
import cv2
import os
import numpy as np

from  camera_pose_estimate  import camPoseEstimate
from  QRCode import MarkerNumError

img = cv2.imread("images/3.jpg")
try:
    camera_pose= camPoseEstimate(img)
    print(camera_pose)
except MarkerNumError:
    print("定位图案识别失败")



