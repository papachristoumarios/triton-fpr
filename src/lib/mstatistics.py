import math

def mean(M):
	"""Arithmetic mean"""
	return sum(M)/len(M)
	
def standard_deviation(M):
	"""Standard deviation"""
	sums = 0
	x_dash = mean(M)
	for t in M:
		sums += (t - x_dash)**2
	return math.sqrt(sums)	
		
def coefficients_of_variation(M):
	"""Coefficients of variation"""
	if len(M) != 0:
		return abs(standard_deviation(M)/mean(M))
	
def get_coefficients_of_variation_dict(D):
	d  = {}
	for k in D.keys():
		d[k] = coefficients_of_variation(D[k])
	return d
