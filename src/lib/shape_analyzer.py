#!/usr/bin/python

#POINTS are of the type (y,x)
import cv2,sys,math
import numpy as np

magnitude = lambda t: math.sqrt(sum(i**2 for i in t))

def get_angle(u,v, asCosine = False,degrees = False):
	cosine = u.dot(v)/(magnitude(v)*magnitude(u))
	if abs(cosine) > 1:
		raise Exception()
		return None
	if asCosine:
		return cosine
	elif not asCosine and not degrees:
		return math.acos(cosine)
	else:
		return math.degrees(math.acos(cosine))
	
def display_multiple_images(images, title):
	nimg = np.hstack(images)
	cv2.imshow(title, nimg)
	
def rectangular_crop(points, ry, rx): 
	points2 = points
	for p in points2:
		if p[0] < ry or p[0] >= len(points2) - ry:
			del(p)
		elif p[1] < rx or p[1] >= len(points2) - rx:
			del(p)
	return points2
	
class ShapeAnalyzer:
	"""Developed for image shape analysis"""

	def __init__(self, image):
		self.image = image
		# Otsu's thresholding after Gaussian filtering
		self.blur = cv2.GaussianBlur(self.image,(5,5),0)
		self.ret,self.th = cv2.threshold(self.blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
		#Canny Edge Detection and second threshold
		self.canny_edges = cv2.Canny(self.th, 0, 255)
		self.ret2,self.th2 = cv2.threshold(self.canny_edges, 127,255, cv2.THRESH_BINARY)		
		self.th2d = self.th2.copy() #for drawing the lines

		#image details
		self.h,self.w = self.th2.shape[:2]
		self.bPoints, self.wPoints = [],[]

		#CAUTION! Points are of the form (y,x)
		# Point filtering
		for i in xrange(self.h):
			for j in xrange(self.w):
				if self.th2.item(i,j) == 0:
					self.bPoints.append((i,j))
				else:
					self.wPoints.append((i,j))
		self.bPoints = np.array(self.bPoints); self.wPoints= np.array(self.wPoints)
		if len(self.wPoints) <= len(self.bPoints):
			self.points = self.wPoints
		else:
			self.points = self.bPoints
		
		#Extreme points
		self.topmost = min(self.points, key = lambda t: t[0])
		self.bottommost = max(self.points, key = lambda t: t[0])
		self.leftmost = min(self.points, key = lambda t: t[1])
		self.rightmost = max(self.points, key = lambda t: t[1])
		
		#Characteristic Vectors
		self.v = np.array(self.topmost) - np.array(self.bottommost)
		self.u = np.array(self.leftmost) - np.array(self.rightmost)
		self.a = np.array(self.topmost) - np.array(self.rightmost)
		self.b = np.array(self.topmost) - np.array(self.leftmost)
		self.c = np.array(self.leftmost) - np.array(self.bottommost)
		self.d = np.array(self.rightmost) - np.array(self.bottommost)
	
		#Length in x and y directions
		self.ly = abs(self.v.dot([1,0]))
		self.lx = abs(self.u.dot([0,1]))
		
		self.__details = ['Height: '+ str(self.h), 'Width: ' + str(self.w), 'Total Length (X): ' + str(self.lx), 'Total Length (Y): ' + str(self.ly)]
			
	def print_details(self):
		for d in details:
			print d
		
	def draw_extreme_points_lines(self):
		#tuples are reversed here
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.bottommost)[::-1],(200,0,0),1)
		cv2.line(self.th2d,tuple(self.leftmost)[::-1],tuple(self.rightmost)[::-1],(200,0,0),1)
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),1)
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),1)
		cv2.line(self.th2d,tuple(self.bottommost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),1)
		cv2.line(self.th2d,tuple(self.bottommost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),1)
	
	def display_steps(self):
		title = 'Shape analysis'
		display_multiple_images((self.image,self.blur,self.th,self.canny_edges,self.th2d),title)
		cv2.waitKey()

	def write_steps(self, _dir):
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'gaussian_blur.jpg', self.blur) 
		cv2.imwrite(_dir + 'otsu_threshold.jpg', self.th) 
		cv2.imwrite(_dir + 'canny_edges.jpg', self.canny_edges) 
		cv2.imwrite(_dir + 'final_image.jpg', self.th2d)
		
	def write_final_image(self, _dir):
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'final_image.jpg', self.th2d)  

	def draw_details(self):
		
		for i in range(len(self.__details)):
			cv2.putText(self.th2d,self.__details[i],(0,20*(i+1)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(200,200,200),1)
		
if __name__ == '__main__':
	img = cv2.imread('/home/marios/1.jpg',0)
	
	s = ShapeAnalyzer(img)
	s.draw_extreme_points_lines()
	s.draw_details()
	#s.display_steps()
	s.write_steps('/home/marios')
