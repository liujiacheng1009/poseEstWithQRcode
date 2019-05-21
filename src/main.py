# Author: Zongchang (Jim) Chen
# Junior at Haverford College, Com-Sci & Math
# Date: Dec, 2016

# main.py 
# Program entrance file. Initialize global variables and call main functions.


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
from camera_pose_estimate import visualize3D
# Import all global constants and coefficients
from settings import *
# Import global model figure
import global_figure as gf
from  camera_pose_estimate  import camPoseEstimate
from QRCode import MarkerNumError

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
# loop over the frames from the video stream


while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    if len(barcodes) :
        try:
            start_time = datetime.datetime.now()  
            camera_pose, camera_orientation,pattern_points = camPoseEstimate(frame)
            pattern_points =np.array(pattern_points,dtype="int")
            for point in pattern_points:
                cv2.circle(frame, tuple(point), 15, (255,0,0), 4)
           # print(pattern_points)
            end_time = datetime.datetime.now()  
            interval = end_time-start_time
            print(camera_pose,interval)
        except MarkerNumError:
            print("MarkerNumError")
        finally:
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the output frame
    cv2.imshow("Barcode Scanner", frame)

    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    if key == ord("p"):
        while((cv2.waitKey(1) & 0xFF) != ord("c")):
            time.sleep(0.1)

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()       

# # Establish global figure
# gf.fig = plt.figure()
# gf.ax = gf.fig.add_subplot(111, projection='3d')

# # Set axes labels
# gf.ax.set_xlabel('X')
# gf.ax.set_ylabel('Y')
# gf.ax.set_zlabel('Z')


# Edit the codes block below to choose images for cam pose estimation.
# You can pick one file only, or severals at the same time.
# You can also write a loop to handle this.
# visualize3D('images/1.jpg')
# visualize3D('images/2.jpg')
# visualize3D('images/3.jpg')
# visualize3D('images/4.jpg')
# visualize3D('images/5.jpg')
# visualize3D('images/6.jpg')
# visualize3D('images/7.jpg')
# visualize3D('images/8.jpg')
# visualize3D('images/9.jpg')


# # Set axes unit length equal, some embellishment
# plt.gca().set_aspect('equal', adjustable='box')

# # Show the plots
# plt.show()










