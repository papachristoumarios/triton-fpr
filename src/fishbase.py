import cv2
import numpy as np


class Fishbase:
	def __init__(self):
		self.members = []
		
	def append_member(self, m):
		self.members.append(m)
		
	def __clear__(self):
		self.members = []
		
	def __add__(self, other):
		self.members = self.members + other.members
		
	def genus_query(self, q):
		for f in self.members
			if f.genus is q:
				print str(f)
		
		
			
		
#fishbase = Fishbase()
	
class Fish:
	
	class Morphometrics:
		"""
		Fish morphometric coefficients:
		cTL: Total Length
		cStL: Standard Length
		cSnL: Snout Length
		cHL: Head Length
		cLCP: Length Caudal Peduncle
		cFL: Fork Length
		"""
		
		def __init__(self, cTL, cStL, cSnL, cHL, cLCP, cFL): 
			self.cTL, self.cStL, self.cSnL, self.cHL, self.cLCP, self.cFL = cTL, cStL, cSnL, cHL, cLCP, cFL
			
	def __init__(self, genus, spieces, bodyClassifier, forkClassifier, headClassifier, cTL, cStL, cSnL, cHL, cLCP, cFL): #TODO Add more classifiers!
		self. genus, self.spieces = genus, spieces
		self.bodyClassifier = cv2.CascadeClassifier(bodyClassifier)
		self.forkClassifier = cv2.CascadeClassifier(forkClassifier)
		self.headClassifier = cv2.CascadeClassifier(headClassifier)
		self.morphometrics = Morphometrics(cTL, cStL, cSnL, cHL, cLCP, cFL)
		self.calTL, self.calStL, self.calSnL, self.calLCP, self.calFL, self.calHL = 0,0,0,0,0,0 #after calculations
		#fishbase.append_member(self)
		
	def morphometrics_cleanup(self):
		self.calTL, self.calStL, self.calSnL, self.calLCP, self.calFL, self.calHL = 0,0,0,0,0,0 #after calculations
	
		
	def isDetectible(self, img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		M = self.bodyClassifier.detectMultiScale(gray, 1.3,5)
		if M is not None:
			return True
		else:
			return False
			
	def applyMorphometrics(self, img):
		if self.isDetectible(img) is True:
			pass 
			#do a cascade.detectMultiScale(args)
			
			
			
					
	
		
		
		
		
	
	


