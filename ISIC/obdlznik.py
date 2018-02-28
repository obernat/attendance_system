#!/usr/bin/env python3

import sys
import numpy as np
import cv2


im = cv2.imread(sys.argv[1])

#hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
#COLOR_MIN = np.array([20, 80, 80],np.uint8)
#COLOR_MAX = np.array([40, 255, 255],np.uint8)
#frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
#imgray = frame_threshed
#ret,thresh = cv2.threshold(frame_threshed,127,255,0)


im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
thresh = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)


_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



# Find the index of the largest contour
areas = [cv2.contourArea(c) for c in contours]
import heapq
max_index = heapq.nlargest(5, range(len(areas)), key=areas.__getitem__)
#max_index = np.argmax(areas)
cnt=contours[max_index[2]]

x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),10)
cv2.imwrite("Show.jpg",im)
