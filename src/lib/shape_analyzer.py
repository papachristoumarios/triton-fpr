#!/usr/bin/python

#POINTS are of the type (y,x)
import cv2,sys,math,random
import numpy as np
from mstatistics import *
	
def midpoint(A,B):
	x = (A[0] + B[0])/2
	y = (A[1] + B[1])/2
	return x,y
	
def get_angle(u,v):
	"""Returns the angle of two vectors"""	
	return (u.dot(v)/(np.linalg.norm(u)*np.linalg.norm(v)))
	
	
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
		self.image = image; self.drawn_img = self.image; self.ratio = 1
		# Otsu's thresholding after Gaussian filtering
		self.blur = cv2.GaussianBlur(self.image,(5,5),0)
		self.ret,self.th = cv2.threshold(self.blur,threshold1,threshold2,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
		#Canny Edge Detection and second threshold
		self.canny_edges = cv2.Canny(self.th, 0, 255)
		self.ret2,self.th2 = cv2.threshold(self.canny_edges, 127,255, cv2.THRESH_BINARY)		

		#image details
		self.h,self.w = self.th2.shape[:2]
		self.bPoints, self.wPoints = [],[]

		indx = np.where(self.th2==0)
		for i,j in zip(indx[0], indx[1]):
			self.bPoints.append((i,j))

		indx = np.where(self.th2==255)
		for i,j in zip(indx[0], indx[1]):
			self.wPoints.append((i,j))
		
		self.bPoints = np.array(self.bPoints)
		self.wPoints =  np.array(self.wPoints)
		
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
		for d in self.details:
			print d
		
	def draw_extreme_points_lines(self,thickness=1):
		"""Draws lines that join the extreme points together"""
		#tuples are reversed here
		cv2.line(self.drawn_img,tuple(self.topmost)[::-1],tuple(self.bottommost)[::-1],(200,0,0),thickness)
		cv2.line(self.drawn_img,tuple(self.leftmost)[::-1],tuple(self.rightmost)[::-1],(200,0,0),thickness)
		cv2.line(self.drawn_img,tuple(self.topmost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),thickness)
		cv2.line(self.drawn_img,tuple(self.topmost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),thickness)
		cv2.line(self.drawn_img,tuple(self.bottommost)[::-1],tuple(self.leftmost)[::-1],(150,0,0),thickness)
		cv2.line(self.drawn_img,tuple(self.bottommost)[::-1],tuple(self.rightmost)[::-1],(150,0,0),thickness)
	
	def display_steps(self):
		"""Displays the shape analysis steps"""
		title = 'Shape analysis'
		display_multiple_images((self.image,self.blur,self.th,self.canny_edges,self.th2d,self.drawn_img),title)
		cv2.waitKey()

	def write_steps(self, _dir):
		"""Exports steps to a directory"""
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'gaussian_blur.jpg', self.blur) 
		cv2.imwrite(_dir + 'otsu_threshold.jpg', self.th) 
		cv2.imwrite(_dir + 'canny_edges.jpg', self.canny_edges) 
		cv2.imwrite(_dir + 'final_image.jpg', self.drawn_img)
		
	def write_final_image(self, _dir):
		"""Writes final image to storage"""
		if not(_dir.endswith('/')):
			_dir = _dir + '/'
		cv2.imwrite(_dir + 'final_image.jpg', self.drawn_img)  

	def draw_details(self):
		"""Draws the details on the image"""
		for i in range(len(self.__details)):
			cv2.putText(self.drawn_img,self.__details[i],(0,20*(i+1)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(200,200,200),1)
			
	def calculate_morphometrics_according_to_specimen(self, fish):
		"""Calculates morphometrics according to specimen"""
		self.TL = max((self.lx,self.ly))
		
		#TL dependent	
		self.HL = fish.morphometrics.cHL * self.TL 
		self.FL = fish.morphometrics.cFL * self.TL
		self.SL = fish.morphometrics.cSL * self.TL 
		self.PdL = fish.morphometrics.cPdL * self.TL
		self.PpL = fish.morphometrics.cPpL * self.TL
		self.PpeL = fish.morphometrics.cPpeL * self.TL
		self.BD = fish.morphometrics.cPpeL * self.TL
		self.PcL = fish.morphometrics.cPcL * self.TL
		self.PoL = fish.morphometrics.cPoL * self.TL
		
		#HL dependent
		self.ED = fish.morphometrics.cED * self.HL
	
	def draw_morphometric_line(self, text, coefficient, point, tilt=(0,0), thickness=2):
		#numpyfied
		try:
			A = point[::-1]
			cx, cy =  np.array((int(coefficient),0)), np.array((0,int(coefficient)))
			tilt = np.array(tilt)
			if point is self.topmost:
				if text is not 'ED':
					B = A + cy
					M = (A + B)/2.0 - (30,0 )
				else:
					A = (A[0], int(A[1] + self.PoL))
					B = (A[0], int(A[1] + self.ED))
					mx,my = midpoint(A,B); mx -= 30; M = (mx,my)
			elif point is self.bottommost:
				B = A - cy
				M = (A + B)/2.0 - (30,0 )

			elif point is self.leftmost:
				B = A + cx
				M = (A+B)/2.0 - (0,30)
			elif point is self.rightmost:	
				B = A - cx
				M = (A+B)/2.0 - (0,30)
			else:
				return
			A += tilt; B+=tilt; M+=tilt; M = M.astype(np.integer)
			c  = random.randint(0,255)
			cv2.line(self.drawn_img, tuple(A), tuple(B), (c,0,0), thickness)
			cv2.putText(self.drawn_img,text,tuple(M), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(c,0,0),1)
		except NameError:
			return
					
	def draw_morphometric_lines_according_to_specimen(self, fish,thickness=2):
		"""Draws morphometrics as lines according to defined specimen"""
		self.calculate_morphometrics_according_to_specimen(fish)

		self.draw_morphometric_line('ED', self.ED, self.topmost, tilt=(10,0))
		self.draw_morphometric_line('PdL', self.PdL, self.topmost, tilt=(5,0))
		self.draw_morphometric_line('PpL', self.PpL, self.topmost, tilt=(15,0))
		self.draw_morphometric_line('PpeL', self.PpeL, self.topmost, tilt=(20,0))
		self.draw_morphometric_line('PoL', self.PoL, self.topmost, tilt=(-5,0))
		self.draw_morphometric_line('HL', self.HL, self.topmost, tilt=(-10,0))
		self.draw_morphometric_line('SL', self.SL, self.topmost, tilt=(-15,0))
		self.draw_morphometric_line('FL', self.FL, self.topmost)


	def export_details_to_CSV(self): #TODO CSV for PostgreSQL 
		pass
		
		
class Contour:
    ''' Provides detailed parameter informations about a contour

        Create a Contour instant as follows: c = Contour(src_img, contour)
                where src_img should be grayscale image.

        Attributes:

        c.area -- gives the area of the region
        c.parameter -- gives the perimeter of the region
        c.moments -- gives all values of moments as a dict
        c.centroid -- gives the centroid of the region as a tuple (x,y)
        c.bounding_box -- gives the bounding box parameters as a tuple => (x,y,width,height)
        c.bx,c.by,c.bw,c.bh -- corresponds to (x,y,width,height) of the bounding box
        c.aspect_ratio -- aspect ratio is the ratio of width to height
        c.equi_diameter -- equivalent diameter of the circle with same as area as that of region
        c.extent -- extent = contour area/bounding box area
        c.convex_hull -- gives the convex hull of the region
        c.convex_area -- gives the area of the convex hull
        c.solidity -- solidity = contour area / convex hull area
        c.center -- gives the center of the ellipse
        c.majoraxis_length -- gives the length of major axis
        c.minoraxis_length -- gives the length of minor axis
        c.orientation -- gives the orientation of ellipse
        c.eccentricity -- gives the eccentricity of ellipse
        c.filledImage -- returns the image where region is white and others are black
        c.filledArea -- finds the number of white pixels in filledImage
        c.convexImage -- returns the image where convex hull region is white and others are black
        c.pixelList -- array of indices of on-pixels in filledImage
        c.maxval -- corresponds to max intensity in the contour region
        c.maxloc -- location of max.intensity pixel location
        c.minval -- corresponds to min intensity in the contour region
        c.minloc -- corresponds to min.intensity pixel location
        c.meanval -- finds mean intensity in the contour region
        c.leftmost -- leftmost point of the contour
        c.rightmost -- rightmost point of the contour
        c.topmost -- topmost point of the contour
        c.bottommost -- bottommost point of the contour
        c.distance_image((x,y)) -- return the distance (x,y) from the contour.
        c.distance_image() -- return the distance image where distance to all points on image are calculated
        '''
    def __init__(self,img,cnt):
        self.img = img
        self.cnt = cnt
        self.size = len(cnt)

        # MAIN PARAMETERS

        #Contour.area - Area bounded by the contour region'''
        self.area = cv2.contourArea(self.cnt)

        # contour perimeter
        self.perimeter = cv2.arcLength(cnt,True)

        # centroid
        self.moments = cv2.moments(cnt)
        if self.moments['m00'] != 0.0:
            self.cx = self.moments['m10']/self.moments['m00']
            self.cy = self.moments['m01']/self.moments['m00']
            self.centroid = (self.cx,self.cy)
        else:
            self.centroid = "Region has zero area"

        # bounding box
        self.bounding_box=cv2.boundingRect(cnt)
        (self.bx,self.by,self.bw,self.bh) = self.bounding_box

        # aspect ratio
        self.aspect_ratio = self.bw/float(self.bh)

        # equivalent diameter
        self.equi_diameter = np.sqrt(4*self.area/np.pi)

        # extent = contour area/boundingrect area
        self.extent = self.area/(self.bw*self.bh)


        ### CONVEX HULL ###

        # convex hull
        self.convex_hull = cv2.convexHull(cnt)

        # convex hull area
        self.convex_area = cv2.contourArea(self.convex_hull)

        # solidity = contour area / convex hull area
        self.solidity = self.area/float(self.convex_area)


        ### ELLIPSE  ###

        self.ellipse = cv2.fitEllipse(cnt)

        # center, axis_length and orientation of ellipse
        (self.center,self.axes,self.orientation) = self.ellipse

        # length of MAJOR and minor axis
        self.majoraxis_length = max(self.axes)
        self.minoraxis_length = min(self.axes)

        # eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
        self.eccentricity = np.sqrt(1-(self.minoraxis_length/self.majoraxis_length)**2)


        ### CONTOUR APPROXIMATION ###

        self.approx = cv2.approxPolyDP(cnt,0.02*self.perimeter,True)


        ### EXTRA IMAGES ###

        # filled image :- binary image with contour region white and others black
        self.filledImage = np.zeros(self.img.shape[0:2],np.uint8)
        cv2.drawContours(self.filledImage,[self.cnt],0,255,-1)

        # area of filled image
        filledArea = cv2.countNonZero(self.filledImage)

        # pixelList - array of indices of contour region
        self.pixelList = np.transpose(np.nonzero(self.filledImage))

        # convex image :- binary image with convex hull region white and others black
        self.convexImage = np.zeros(self.img.shape[0:2],np.uint8)
        cv2.drawContours(self.convexImage,[self.convex_hull],0,255,-1)


        ### PIXEL PARAMETERS
      
        # mean value, minvalue, maxvalue
        self.minval,self.maxval,self.minloc,self.maxloc = cv2.minMaxLoc(self.img,mask = self.filledImage)
        self.meanval = cv2.mean(self.img,mask = self.filledImage)


        ### EXTREME POINTS ###

        # Finds the leftmost, rightmost, topmost and bottommost points
        self.leftmost = tuple(self.cnt[self.cnt[:,:,0].argmin()][0])
        self.rightmost = tuple(self.cnt[self.cnt[:,:,0].argmax()][0])
        self.topmost = tuple(self.cnt[self.cnt[:,:,1].argmin()][0])
        self.bottommost = tuple(self.cnt[self.cnt[:,:,1].argmax()][0])
        self.extreme = (self.leftmost,self.rightmost,self.topmost,self.bottommost)

    ### DISTANCE CALCULATION
  
    def distance_image(self,point=None):
      
        '''find the distance between a point and adjacent point on contour specified. Point should be a tuple or list (x,y)
            If no point is given, distance to all point is calculated and distance image is returned'''
        if type(point) == tuple:
            if len(point)==2:
                self.dist = cv2.pointPolygonTest(self.cnt,point,True)
                return self.dist
        else:
            dst = np.empty(self.img.shape)
            for i in xrange(self.img.shape[0]):
                for j in xrange(self.img.shape[1]):
                    dst.itemset(i,j,cv2.pointPolygonTest(self.cnt,(j,i),True))

            dst = dst+127
            dst = np.uint8(np.clip(dst,0,255))

            # plotting using palette method in numpy
            palette = []
            for i in xrange(256):
                if i<127:
                    palette.append([2*i,0,0])
                elif i==127:
                    palette.append([255,255,255])
                elif i>127:
                    l = i-128
                    palette.append([0,0,255-2*l])
            palette = np.array(palette,np.uint8)
            self.h2 = palette[dst]
            return self.h2

	def demonstrate():
	   
	    if len(sys.argv)>1:
	        image = sys.argv[1]
	    else:
	        image = 'new.bmp'
	        print "Usage : python contourfeatures.py <image_file>"
	  
	    im = cv2.imread(image)
	    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	    thresh = cv2.adaptiveThreshold(imgray,255,0,1,11,2)
	    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	    k = 1000
	    for cnt in contours:
	
	        # first shows the original image
	        im2 = im.copy()
	        c = Contour(imgray,cnt)
	        print c.leftmost,c.rightmost
	        cv2.putText(im2,'original image',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))       
	        cv2.imshow('image',im2)
	        if cv2.waitKey(k)==27:
	            break
	      
	        im2 = im.copy()
	
	        # Now shows original contours, approximated contours, convex hull
	        cv2.drawContours(im2,[cnt],0,(0,255,0),4)
	        string1 = 'green : original contour'
	        cv2.putText(im2,string1,(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
	        cv2.imshow('image',im2)
	        if cv2.waitKey(k)==27:
	            break
	      
	        approx = c.approx
	        cv2.drawContours(im2,[approx],0,(255,0,0),2)
	        string2 = 'blue : approximated contours'
	        cv2.putText(im2,string2,(20,40), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
	        cv2.imshow('image',im2)
	        if cv2.waitKey(k)==27:
	            break
	      
	        hull = c.convex_hull
	        cv2.drawContours(im2,[hull],0,(0,0,255),2)
	        string3 = 'red : convex hull'
	        cv2.putText(im2,string3,(20,60), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
	        cv2.imshow('image',im2)
	        if cv2.waitKey(k)==27:
	            break
	
	        im2 = im.copy()
	
	        # Now mark centroid and bounding box on image
	        (cx,cy) = c.centroid
	        cv2.circle(im2,(int(cx),int(cy)),5,(0,255,0),-1)
	        cv2.putText(im2,'green : centroid',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
	
	        (x,y,w,h) = c.bounding_box
	        cv2.rectangle(im2,(x,y),(x+w,y+h),(0,0,255))
	        cv2.putText(im2,'red : bounding rectangle',(20,40), cv2.FONT_HERSHEY_PLAIN, 1.0,(0,255,0))
	
	        (center , axis, angle) = c.ellipse
	        cx,cy = int(center[0]),int(center[1])
	        ax1,ax2 = int(axis[0]),int(axis[1])
	        orientation = int(angle)
	        cv2.ellipse(im2,(cx,cy),(ax1,ax2),orientation,0,360,(255,255,255),3)
	        cv2.putText(im2,'white : fitting ellipse',(20,60), cv2.FONT_HERSHEY_PLAIN, 1.0,(255,255,255))
	
	        cv2.circle(im2,c.leftmost,5,(0,255,0),-1)
	        cv2.circle(im2,c.rightmost,5,(0,255,0))
	        cv2.circle(im2,c.topmost,5,(0,0,255),-1)
	        cv2.circle(im2,c.bottommost,5,(0,0,255))
	        cv2.imshow('image',im2)
	        if cv2.waitKey(k)==27:
	            break
	
	      
	        # Now shows the filled image, convex image, and distance image
	        filledimage = c.filledImage
	        cv2.putText(filledimage,'filledImage',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,255)
	        cv2.imshow('image',filledimage)
	        if cv2.waitKey(k)==27:
	            break
	
	        conveximage = c.convexImage
	        cv2.putText(conveximage,'convexImage',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,255)
	        cv2.imshow('image',conveximage)
	        if cv2.waitKey(k)==27:
	            break
		
	        distance_image = c.distance_image()
	        cv2.imshow('image',distance_image)
	        cv2.putText(distance_image,'distance_image',(20,20), cv2.FONT_HERSHEY_PLAIN, 1.0,(255,255,255))
	        if cv2.waitKey(k)==27:
	            break
	      
	cv2.destroyAllWindows()
	

	
if __name__ == '__main__':
	img = cv2.imread('/home/marios/2.jpg',0)
	from fish import Fish
	#a dumb fish
	f1 = Fish(name='f1')
	f1.morphometrics.cHL = 0.3
	f1.morphometrics.cSL = 0.7
	f1.morphometrics.cFL = 0.7
	f1.morphometrics.cPoL = 0.2
	f1.morphometrics.cED = 0.05
	s = ShapeAnalyzer(img)
	s.draw_extreme_points_lines()
	#s.draw_details()
	s.draw_morphometric_lines_according_to_specimen(f1)
	s.write_steps('/home/marios')
	print s.TL
	print s.HL
	print s.area
	print s.rhombus_area
	print s.mean_area
	print s.area_standard_deviation
