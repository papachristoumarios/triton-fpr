#!/usr/bin/env python2.7
#wrapper module for libdetectors.so

import os
import ctypes as c

libDETECTORS = c.cdll.LoadLibrary('./libdetectors.so')

class CExternalMatchesFunction:
	
	def __init__(self, c_func):
		self.c_func = c_func
		self.c_func.argtypes = [c.c_char_p, c.c_char_p]
		self.c_func.restype = c.c_int
		
	def __call__(self, train_img_filename, query_img_filename):
		r = self.c_func(c.c_char_p(train_img_filename), c.c_char_p(query_img_filename))
		return r

#initialize wrapped functions				
get_matches_sift_flann = CExternalMatchesFunction(libDETECTORS.get_matches_sift_flann)
		

if __name__ == '__main__':
	
	print get_matches_sift_flann("/home/marios/1.jpg","/home/marios/4.jpg")
