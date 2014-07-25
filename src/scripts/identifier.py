#scripts.detect.detect2 returns:
# elements[4] [0]: image, [1]: NOF, [2]: true if found, [3]:coordinates

def identify(image, base, detectCharacteristics = False):
	artifacts = {}
	for f in base:
		elems = detector.detect2(image,f.bodycascade)
		if elems[2]:
			print 'Found: {0} Quantity: {1}'.format(str(f),elems[1])
			print 'Coordinates:' + str(elems[3])
			artifacts[str(f)] = elems[1]
			if detectCharacteristics: #characteristics identification
				for i in range(0, len(elems[3])):
					x = elems[3][i][0]
					y = elems[3][i][1]
					w = elems[3][i][2]
					h = elems[3][i][3]
					roi = image[x: x+w, y: y+h]
					for j in len(0,f.fcascades):
						roi_elems = detector.detect2(image,f.fcascades[j])
						print '{0} --> Feature: {1} Quantity: {2}'.format(i, j, roi_elems[1])
						print 'Coordinates: ' + str(roi_elems[1])
	return artifacts									
				
class ComplexIdentification:
	
	def calculate_probability(img_freq,geo_freq):
		from math import sqrt
		return sqrt(img_freq**2 + geo_freq**2)		
			
#TODO Add main method for tests



