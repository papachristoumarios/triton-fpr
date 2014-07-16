#!/usr/bin/python

import cv2; import numpy as np

def translate(img, tx, ty):
	
	rows,cols = img.shape

	M = np.float32([[1,0,tx],[0,1,ty]])
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst
	
def rotate(img, a):
	rows,cols = img.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),a,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst
	

