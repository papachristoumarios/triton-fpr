#!/usr/bin/env python2.7

import numpy as np
import cv2, glob, mstatistics, os

global orb, sift, CV_HOMOGENITY_COEFFICIENT
orb = cv2.ORB(); sift = cv2.SIFT()
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
			self.cv = mstatistics.coefficients_of_variation(matches)
			if check_homogenity:
				if self.cv <= CV_HOMOGENITY_COEFFICIENT:
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
			
class BruteForceSIFTFeatureMatching:
	class ImageSet:
		def __init__(self, name, directory, ext='.jpg'):
			self.name, self.directory, self.images = name, directory, []
			images_list = glob.glob('{0}/*{1}'.format(directory,ext))
			self.sift = sift
			for _img in images_list:
				img = cv2.imread(_img,0); self.images.append(img)
					
		def get_matches(self, query_image,check_homogenity=False,k=2):
			good_matches = []
			for image in self.images:
				kp1, des1 = self.sift.detectAndCompute(query_image,None)
				kp2, des2 = self.sift.detectAndCompute(image,None)
				# BFMatcher with default params
				bf = cv2.BFMatcher()
				matches = bf.knnMatch(des1,des2, k=k)
				# Apply ratio test
				good = []
				for m,n in matches:
					if m.distance < 0.75*n.distance:
						good.append([m])	
			good_matches.append(len(good))
			self.cv = mstatistics.coefficients_of_variation(good_matches)

			if len(good_matches) == 0:
				return 0
			if check_homogenity:
				if self.cv <= CV_HOMOGENITY_COEFFICIENT:
					return mstatistics.mean(good_matches)
				else:
					return 0
			else:
				return [mstatistics.mean(good_matches), max(good_matches)]
		
	def __init__(self, image_sets = []):
		self.sift = sift
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
		
class SIFTHolographyFeatureMatching:
	class ImageSet:
		def __init__(self, name, directory, ext='.jpg'):
			self.name, self.directory, self.images = name, directory, []
			images_list = glob.glob('{0}/*{1}'.format(directory,ext))
			self.sift = sift
			for _img in images_list:
				img = cv2.imread(_img,0); self.images.append(img)
					
		def get_matches(self, query_image,check_homogenity=False,k=2):
			good_matches = []
			for image in self.images:
				kp1, des1 = self.sift.detectAndCompute(query_image,None)
				kp2, des2 = self.sift.detectAndCompute(image,None)
				FLANN_INDEX_KDTREE = 0
				index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
				search_params = dict(checks = 50)
				flann = cv2.FlannBasedMatcher(index_params, search_params)
				matches = flann.knnMatch(des1,des2,k=2)
				good = []
				
				for m,n in matches:
					if m.distance < 0.7*n.distance:
						good.append(m)
			good_matches.append(len(good))
			self.cv = mstatistics.coefficients_of_variation(good_matches)

			if len(good_matches) == 0:
				return 0
			if check_homogenity:
				if self.cv <= CV_HOMOGENITY_COEFFICIENT:
					return mstatistics.mean(good_matches)
				else:
					return 0
			else:
				return [mstatistics.mean(good_matches), max(good_matches)]
		
	def __init__(self, image_sets = []):
		self.sift = sift
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
	import time
	t1 = time.time()
	q = cv2.imread('../../data/test-images/2.jpg',0)

	s1 = BruteForceSIFTFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/pagellus_erythrinus')
	s2 = BruteForceSIFTFeatureMatching().ImageSet('M.B', '../../data/train-images/mullus_barbatus')
	s3 = BruteForceSIFTFeatureMatching().ImageSet('H.D', '../../data/train-images/helicolenus_dactylopterus')
	s4 = BruteForceSIFTFeatureMatching().ImageSet('S.C', '../../data/train-images/scyliorhinus_canicula')
	s = [s1,s2,s3,s4]
	b = BruteForceSIFTFeatureMatching(s)
	b.identify(q)
	
	h1 = SIFTHolographyFeatureMatching().ImageSet('Pagellus Erythrinus', '../../data/train-images/pagellus_erythrinus')
	h2 = SIFTHolographyFeatureMatching().ImageSet('M.B', '../../data/train-images/mullus_barbatus')
	h3 = SIFTHolographyFeatureMatching().ImageSet('H.D', '../../data/train-images/helicolenus_dactylopterus')
	h4 = SIFTHolographyFeatureMatching().ImageSet('S.C', '../../data/train-images/scyliorhinus_canicula')
	h = [h1,h2,h3,h4]
	H = SIFTHolographyFeatureMatching(h)
	H.identify(q)
	

