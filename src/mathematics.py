from math import sqrt,cos,sin,atan

class Point:
	
	def __init__(self, x,y):
		self.x = x; self.y = y
		
	def getDistance(self):
		return sqrt(self.x**2 + self.y**2)
		
class Vector(Point):
			
	def __init__(self, A=None,B):
		if A is None:
			A.x, B.x = 0,0
		self.x = B.x - A.x; self.y = B.y - A.y
		
	def getMagnitude(self):
		return sqrt(self.x**2 + self.y**2)
		
