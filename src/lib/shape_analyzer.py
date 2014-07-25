#!/usr/bin/python

#POINTS are of the type (y,x)
import cv2,sys,math
import numpy as np

def mean(M):
	return sum(M)/len(M)

def standard_deviation(M,squared=False):
	sums = 0
	x_dash = mean(M)
	for t in M:
		sums += (t - x_dash)**2
		
def coefficients_of_variation(M):
	return abs(standard_deviation(M) / mean(M))
	
	s2 = sums / len(M)
	if squared:
		return s2
	else:
		return math.sqrt(s2)
		
def get_angle(u,v, asCosine = False,degrees = False):
	"""Returns the angle of two vectors"""
	cosine = u.dot(v)/(np.linalg.norm(v)*np.linalg.norm(u))
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
	"""Display multiple images via the numpy hstack() function"""
	nimg = np.hstack(images)
	cv2.imshow(title, nimg)
	
def rectangular_crop(points, ry, rx): 
	"""Perform a rectangular crop to points of the type (y,x)"""
	points2 = points
	for p in points2:
		if p[0] < ry or p[0] >= len(points2) - ry:
			del(p)
		elif p[1] < rx or p[1] >= len(points2) - rx:
			del(p)
	return points2
	
class ShapeAnalyzer:
	"""Developed for image shape analysis"""

	def __init__(self, image, threshold1=0,threshold2=255):
		"""ShapeAnalyzer Class Constructor. It generates results by performing:
		1. a Gaussian Blur filter
		2. Otsu's Threshold and Binary Threshold
		3. Canny Edge Detection
		4. Second binary threshold
		5. calculations to find extreme points (TM,BM,LM,RM)
		Besides this, it:
		6. computes four characteristic vectors connecting the extreme points
		7. finds the area of the formed polygon via cross product
		8. finds total length in XY directions via dot product with the base vectors i=[0,1] j=[1,0] if points have type of (y,x)		
		"""
		self.image = image
		# Otsu's thresholding after Gaussian filtering
		self.blur = cv2.GaussianBlur(self.image,(5,5),0)
		self.ret,self.th = cv2.threshold(self.blur,threshold1,threshold2,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
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
		self.a = - (np.array(self.topmost) - np.array(self.rightmost))
		self.b = - (np.array(self.topmost) - np.array(self.leftmost))
		self.c = - (np.array(self.leftmost) - np.array(self.bottommost))
		self.d = - (np.array(self.rightmost) - np.array(self.bottommost))
	
		#area of polygon defined by the vectors a,b,c,d

	
		#Length in x and y directions
		self.ly = abs(self.v.dot([1,0]))
		self.lx = abs(self.u.dot([0,1]))
		
		self.__details = ['Height: '+ str(self.h), 'Width: ' + str(self.w), 'Total Length (X): ' + str(self.lx), 'Total Length (Y): ' + str(self.ly)]
			
		self.area = 0.5 * (np.linalg.norm(np.cross(self.a,self.b)) + np.linalg.norm(np.cross(self.c,self.d)))
		self.rhombus_area = 0.5*(self.lx*self.ly)
		self.mean_area = mean([self.area, self.rhombus_area])
		self.area_standard_deviation = standard_deviation([self.area, self.rhombus_area])	
			
	def print_details(self):
		"""Print shape analysis results"""
		for d in details:
			print d
		
	def draw_extreme_points_lines(self,thickness=1):
		"""Draws lines that join the extreme points together"""
		#tuples are reversed here
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.bottommost)[::-1],(200,0,0),thickness)
		cv2.line(self.th2d,tuple(self.leftmost)[::-1],tuple(self.rightmost)[::-1],(200,0,0),thickness)
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),thickness)
		cv2.line(self.th2d,tuple(self.topmost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),thickness)
		cv2.line(self.th2d,tuple(self.bottommost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),thickness)
		cv2.line(self.th2d,tuple(self.bottommost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),thickness)
	
	def display_steps(self):
		"""Displays the shape analysis steps"""
		title = 'Shape analysis'
		display_multiple_images((self.image,self.blur,self.th,self.canny_edges,self.th2d),title)
		cv2.waitKey()

	def write_steps(self, _dir):
		"""Exports steps to a directory"""
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'gaussian_blur.jpg', self.blur) 
		cv2.imwrite(_dir + 'otsu_threshold.jpg', self.th) 
		cv2.imwrite(_dir + 'canny_edges.jpg', self.canny_edges) 
		cv2.imwrite(_dir + 'final_image.jpg', self.th2d)
		
	def write_final_image(self, _dir):
		"""Writes final image to storage"""
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'final_image.jpg', self.th2d)  

	def draw_details(self):
		"""Draws the details on the image"""
		for i in range(len(self.__details)):
			cv2.putText(self.th2d,self.__details[i],(0,20*(i+1)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(200,200,200),1)
			
	def calculate_morphometrics_according_to_specimen(self, fish):
		"""Calculates morphometrics according to specimen"""
		if self.lx > self.ly:
			self.TL = self.lx
		else:
			self.TL = self.ly
			
		self.HL = fish.morphometrics.cHL * self.TL
		self.FL = fish.morphometrics.cFL * self.TL
		self.SL = fish.morphometrics.cSL * self.TL #NOT SURE
		
	def draw_morphometric_lines_according_to_specimen(self, fish,thickness=2):
		"""Draws morphometrics as lines according to defined specimen"""
		self.calculate_morphometrics_according_to_specimen(fish)
		cv2.line(self.th2d,tuple(self.topmost)[::-1],(self.topmost[1], int(self.topmost[0] + self.HL)),(200,0,0),thickness)
		cv2.line(self.th2d,tuple(self.bottommost)[::-1], (self.bottommost[1], int(self.bottommost[0] - self.FL)), (200,0,0),thickness)

	def export_details_to_CSV(self): #TODO CSV for PostgreSQL 
		pass
		
				
if __name__ == '__main__':
	img = cv2.imread('/home/marios/1.jpg',0)
	from fish import Fish
	#a dumb fish
	f1 = Fish('f1',cHL = 0.25, cFL = 0.3, cSL = 0.1)
	s = ShapeAnalyzer(img)
	s.draw_extreme_points_lines()
	s.draw_details()
	s.draw_morphometric_lines_according_to_specimen(f1)
	s.draw_morphometric_lines_according_to_specimen(f1)
	#s.write_steps('/home/marios/Dropbox')
	print s.area
	print s.rhombus_area
	print s.mean_area
	print s.area_standard_deviation
