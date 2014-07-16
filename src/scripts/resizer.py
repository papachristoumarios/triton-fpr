#!/usr/bin/python

import cv2,sys, Image, os
import numpy as np

__doc__ = '''Usage: ./resizer.py dir1/ <scale factor>'''

def resize_images_in_directory(input_dir, scale_factor, replace=True):
	os.chdir(input_dir)
	filelist = os.listdir('.')
	for e in filelist:
		try:
			Image.open(e)
			img = cv2.imread(e)
			h,w = img.shape[:2]
			rimg = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
			if not(replace):
				e = 'scaled_' + e
			cv2.imwrite(e, rimg)
			
		except IOError:	
			pass 

if __name__ == '__main__':
	_indir = sys.argv[1]
	_sf = float(sys.argv[2])
	resize_images_in_directory(_indir, _sf, replace=True)
	print 'Done'
	
	
