# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import cv2
import numpy as np


def dom (image, sample):

    coordinates = None
    mom = None
    text = "No"

    gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_im = cv2.GaussianBlur(gray_im, (21, 21), 0)

    gray_sp = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    gray_sp = cv2.GaussianBlur(gray_sp, (21, 21), 0)


    frame_delta = cv2.absdiff(gray_sp, gray_im)
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # loop over the contours
    if len(cnts) != 0:
        cnt_max = max(cnts, key = cv2.contourArea)
        if cv2.contourArea(cnt_max) >= 1000:
            coordinates = cv2.boundingRect(cnt_max) 
            text = "Yes"

            M = cv2.moments(cnt_max)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            mom = (cx, cy)

    return coordinates, mom
