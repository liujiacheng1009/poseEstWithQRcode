from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# from camera_pose_estimate import visualize3D
# from settings import *
# import global_figure as gf
# from  camera_pose_estimate  import camPoseEstimate
# from QRCode import MarkerNumError


img = cv2.imread("images/qrcode3.png")
barcodes = pyzbar.decode(img)
for barcode in barcodes:
    (x,y,w,h) = barcode.rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(img, text, (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
cv2.imshow("Barcode Scanner",img)
