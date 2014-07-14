#!/usr/bin/python
import os,sys, cv2
from PIL import Image
import numpy as np

"""A small script for converting images from user-defined directories to grayscale"""


__doc__ = ''' Usage: ./grayscaler.py /dir/of/images'''

def main(in_dir):
	os.chdir(in_dir)
	filelist = os.listdir('.')
	for e in filelist:
		try:
			Image.open(e)
			img = cv2.imread(e)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(e, img)
		except IOError:
			print '{0} is not a valid image'.format(e)
			continue 	
	
if __name__ == '__main__':
	if len(sys.argv) is not 2:
		raise Exception('Bad input')
		print __doc__
		exit()
	else:
		input_dir = sys.argv[1]
		main(input_dir)
