# import the necessary packages
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

image = cv2.imread("images/qrcode3.png")
barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw the barcode data and barcode type on the image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


plt.imshow(image)
plt.title("Raw image")
plt.axis("off")
plt.show()
