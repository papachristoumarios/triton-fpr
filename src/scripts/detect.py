#!/usr/bin/python

import sys
import cv,cv2
import numpy

"""Feature detector"""
__doc__ = '''Usage: ./detect.py /dir/image.jpg /dir2/cascade.xml'''

def detect(image,cascade):
	"""OBSOLETE: Uses cv (v1)"""
	bitmap = cv.fromarray(image)
	faces = cv.HaarDetectObjects(bitmap, cascade, cv.CreateMemStorage(0))
	if faces:
		for (x,y,w,h),n in faces:  
			cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),3)
	return image

	
def detect2(image, cascade):
	features = cascade.detectMultiScale(image)
	if len(features) is not 0:
		for (x,y,w,h) in features:
			cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,255), 3)
		elems = [image, len(features), True, features]
	else:
		elems = [0,0,False,0]
	return elems

if __name__ == "__main__":
	if len(sys.argv) is not 3:
		raise Exception('Bad Input')
		exit()
	else:
		cascade = cv2.CascadeClassifier(sys.argv[2])
		img = cv2.imread(sys.argv[1])
		elements  = detect2(img, cascade)
		title = 'Found {0} matches'.format(elements[1])
		cv2.imshow(title, img)
		print title
		for e in elements[3]:
			print str(e)
			
			
		cv2.waitKey()
