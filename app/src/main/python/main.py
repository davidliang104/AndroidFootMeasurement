from sklearn.cluster import KMeans
import random as rng
import cv2
import imutils
import argparse
from imutils import contours
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt
import os
from com.chaquo.python import Python

from utils import *


#ImgPath = 'data/barefeet1.jpeg'


def main(img):
    oimg = cv2.imdecode(np.asarray(img, dtype=np.uint8), cv2.IMREAD_COLOR)
    preprocessedOimg = preprocess(oimg)

   # oimg = imread(ImgPath)

    #output = os.path.join(os.environ["HOME"], 'output')

    files = Python.getPlatform().getApplication().getFilesDir()
    output = os.path.join((str)(files), 'output')

    if not os.path.exists(output):
        os.makedirs(output)


    cv2.imwrite(output + '/preprocessedOimg.jpg', preprocessedOimg)
    print(output + '/preprocessedOimg.jpg')

    clusteredImg = kMeans_cluster(preprocessedOimg)
    cv2.imwrite(output + '/clusteredImg.jpg', clusteredImg)

    edgedImg = edgeDetection(clusteredImg)
    cv2.imwrite(output + '/edgedImg.jpg', edgedImg)

    boundRect, contours, contours_poly, img = getBoundingBox(edgedImg)
    pdraw = drawCnt(boundRect[1], contours, contours_poly, img)
    cv2.imwrite(output + '/pdraw.jpg', pdraw)


    croppedImg, pcropedImg = cropOrig(boundRect[1], clusteredImg)
    cv2.imwrite(output + '/croppedImg.jpg', croppedImg)


    newImg = overlayImage(croppedImg, pcropedImg)
    cv2.imwrite(output + '/newImg.jpg', newImg)

    fedged = edgeDetection(newImg)
    fboundRect, fcnt, fcntpoly, fimg = getBoundingBox(fedged)
    fdraw = drawCnt(fboundRect[2], fcnt, fcntpoly, fimg)
    cv2.imwrite(output + '/fdraw.jpg', fdraw)

    return "feet size (cm): " + (str)(calcFeetSize(pcropedImg, fboundRect)/10)