from pyzbar import pyzbar
import argparse
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import pickle


img = cv2.imread("images/qrcode3.png")
data = (50, 150)
imgCanny = cv2.Canny(img, *data)

plt.subplot(211)
plt.imshow(img)
plt.title("Raw image")
plt.axis("off")
plt.subplot(212)
plt.imshow(imgCanny)
plt.title("Corrected image")
plt.axis("off")
plt.show()