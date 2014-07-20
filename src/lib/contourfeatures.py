import cv2
import numpy as np

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


#### DEMO ######
if __name__=='__main__':

    import sys
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
