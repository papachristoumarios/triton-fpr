#!/usr/bin/env python2.7

import numpy as np
import cv2, glob, mstatistics, os

global orb, CV_HOMOGENITY_COEFFICIENT
orb = cv2.ORB()
CV_HOMOGENITY_COEFFICIENT = 0.15

class BruteForceORBFeatureMatching:
	class ImageSet:
		def __init__(self, name, directory, ext='.jpg'):
			self.name, self.directory, self.images = name, directory, []
			images_list = glob.glob('{0}/*{1}'.format(directory,ext))
			self.orb = orb
			for _img in images_list:
				img = cv2.imread(_img,0); self.images.append(img)
					
		def get_matches(self, query_image,check_homogenity=True):
			matches = []
			for image in self.images:
				kp1, des1 = self.orb.detectAndCompute(query_image,None)
				kp2, des2 = self.orb.detectAndCompute(image,None)
			
				# create BFMatcher object
				bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
				# Match descriptors.
				_matches = bf.match(des1,des2)
				matches.append(len(_matches))
				# Sort them in the order of their distance.
				#_matches = sorted(_matches, key = lambda x:x.distance)
			if len(matches) == 0:
				return 0
			if check_homogenity:
				cv = mstatistics.coefficients_of_variation(matches)
				if cv <= CV_HOMOGENITY_COEFFICIENT:
					return mstatistics.mean(matches)
				else:
					return 0
			else:
				return [mstatistics.mean(matches), max(matches)]
		
	def __init__(self, image_sets = []):
		self.orb = orb
		self.image_sets = image_sets
		
	def append_image_set(self, s):
		self.image_sets.append(s)
	
	def compare_matches(self, query_image):
		M = {}
		for image_set in self.image_sets:
			M[image_set.get_matches(query_image)[1]] = image_set 
		return M[max(M.keys())]
		
	def identify(self, query_image):
		result = self.compare_matches(query_image)
		print result.name

if __name__ == '__main__':
	s1 = BruteForceORBFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/pagellus_erythrinus')
	s2 = BruteForceORBFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/mullus_barbatus')
	s3 = BruteForceORBFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/helicolenus_dactylopterus')
	s4 = BruteForceORBFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/scyliorhinus_canicula')
	s = [s1,s2,s3,s4]
	b = BruteForceORBFeatureMatching(s)
	b.identify(cv2.imread('../../data/test-images/2.jpg',0))
