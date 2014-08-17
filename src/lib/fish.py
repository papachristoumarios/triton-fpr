from detectors import *

class Fish:
	"""Stores info for each fish"""
	def __init__(self, name='', bodycascade=None, fcascades = []):
		self.name = name; self.bodycascade = bodycascade;
		self.fcascades = fcascades
		self.morphometrics = Morphometrics()
		self.code = None
		self.images_dir, self.image_set = '', None
		
	def __str__(self):
		return self.name
		
	def get_morphometrics(self):
		names =   {'Head Length' : self.morphometrics.cHL,
					'Fork Length' : self.morphometrics.cFL,
					'Standard Length': self.morphometrics.cSL,
					'Pre-dorsal Length': self.morphometrics.cPdL,
					'Pre-pelvic Length': self.morphometrics.cPpL,
					'Pre-pectoral Length': self.morphometrics.cPpeL,
					'Body depth': self.morphometrics.cBD,
					'Pre-orbital Length': self.morphometrics.cPoL,
					'Pre-caudial fin Length': self.morphometrics.cPcL,
					'Pre-anal Length': self.morphometrics.cPaL}
		result = ''''''				
		for k in names.keys():
			result += '{0} : {1} of TL\n'.format(k,names[k])
		return result
			
class Morphometrics(Fish):
	"""Morphometrics are stored at this class"""
	def __init__(self, cHL=0, cFL=0, cSL=0, cPdL=0, cPpL=0, cPpeL=0,cBD=0, cPoL=0, cPcL=0, cED=0, cPaL=0):
		self.cHL, self.cFL, self.cSL, self.cPdL, self.cPpL, self.cPpeL, self.cBD, self.cPoL, self.cPcL, self.cED, self.cPaL =  cHL, cFL, cSL, cPdL, cPpL, cPpeL, cBD, cPoL, cPcL, cED, cPaL

class Database:
	"""Handle PostgreSQL databases"""
	def __init__(self, datasource_url):
		"""Initializes a connection and its cursor using the psycopg2 module for talking with Postgres databases""" 	
		import psycopg2 
		self.connection = psycopg2.connect(datasource_url)
		self.cursor = self.connection.cursor()
		
	def execute(self, cmd):
		"""Executes a command"""
		self.cursor.execute(cmd)
	
	def query(self,q):
		"""Runs a query and fetches all the information"""
		self.cursor.execute(q)
		return self.cursor.fetchall()

class FishDatabase(Database):
	"""Database for fishes"""	
	def __init__(self, datasource_url):
		self.members = []
		self.db = Database(datasource_url)
		self.species_list = self.db.query('SELECT * FROM "FISHES_PARAM"')
		print 'Species list populated succesfully'
	
	def append_member(self, m):
		"""Appends member to database"""
		self.members.append(m)
				
	def query_morphometrics(self, code, morph):
		"""Returns morphometric value according to specimen's code and morphometric code"""
		r = self.db.query('''SELECT * FROM "MORPHOMETRICS_MASTER" WHERE "CD_SPECIES"='{0}' AND "CD_COEFFICIENT"='{1}'; '''.format(code,morph))
		if len(r) is 0:
			return 0
		elif len(r) is 1:
			return r[0][2] 
		else: #return avg
			s = 0
			for e in r:
				s += e[2]
			return s/len(r)
			
	def query_cascade(self, code, casc):
		"""Returns a cascade (.xml file) from the FishDatabase according to specimen's code and cascade's code"""
		r = self.db.query('''SELECT * FROM "CASCADE_MASTER" WHERE "CD_SPECIES"='{0}' AND "CD_CASCADE"='{1}'; '''.format(code,casc))
		if len(r) is 0:
			return None
		else:
			return r[0][2]
			
	def query_feature_cascades(self, code):
		"""Returns feature cascades from the FishDatabase according to specimen's code"""
		r = self.db.query('''SELECT * FROM "CASCADE_MASTER" WHERE "CD_SPECIES"='{0}' AND "CD_CASCADE"!='BC';'''.format(code))
		features = []
		if len(r) is 0:
			return [()]
		else:
			for e in r:
				features.append(r[1:])
			return features #returns feature name, xml-dir
			
	def query_code(self, code, name=False):
		"""Returns a member of the database depending on its code"""
		for m in self.members:
			if m.code is code:
				if name:
					return m.name
				return m
		return None
		
	def query_images_dir(self, code):
		"""Returns the images directory using an SQL query""" 
		r = self.db.query('''SELECT * FROM "IMAGES_DIR" WHERE "CD_SPECIES"='{0}';'''.format(code))
		try:
			return r[0][2]
		except IndexError:
			return None
		
	#open image in 0 mode
	def identify(self,img, draw=False, detectCharacteristics=False):
		"""DEPRECATED: Please use identify2. Performs the identification process based on Haar-like features from the members of 'this' base. Returns a Fish if found, otherwise None"""
		import cv2; timg = img.copy()
		for m in self.members:
			cascade = cv2.CascadeClassifier(m.bodycascade)
			features = cascade.detectMultiScale(img)
			if len(features) is not 0:
				print m.code, m.name, 'found'
				if draw:
					for (x,y,w,h) in features:
						timg = cv2.rectangle(timg, (x,y), (x+w,y+h), (255,0,0), 2)
						if detectCharacteristics:
							roi = timg[y:y+h, x:x+w]
							for f in m.fcascades:
								_cascade = cv2.CascadeClassifier(f)
								_features = f.detectMultiScale(roi)
								for (fx,fy,fw,fh) in _features:
									cv2.rectangle(roi, (fx,fy), (fx+fw, fy+fh), (255,0,0), 2)
				return m
		return None 
		
	def identify2(self, img, mode='BFORB', cv_check=False):
		"""Performs Identification process. Please specify 'mode' as:
		1. BFORB for Brute-force matching with  ORB Features
		2. BFORB for Brute-force matching SIFT Features
		3. SIFTH for SIFT and Holography Feature Detection"""
		d = {}
		if mode == 'BFORB':
			for m in self.members:
				if m.images_dir != None:
					m.image_set = BruteForceORBFeatureMatching().ImageSet(m.name, m.images_dir)
					d[m.image_set.get_matches(img,check_homogenity=cv_check)[1]] = m
			r =  d[max(d.keys())]
			print r.code, r.name, 'found'
			return r
		elif mode == 'BFSIFT':
			for m in self.members:
				if m.images_dir != None:
					m.image_set = BruteForceSIFTFeatureMatching().ImageSet(m.name, m.images_dir)
					d[m.image_set.get_matches(img,check_homogenity=False)[1]] = m
			r =  d[max(d.keys())]
			print r.code, r.name, 'found'
			return r
		elif mode == 'SIFTH':
			for m in self.members:
				if m.images_dir != None:
					m.image_set = SIFTHolographyFeatureMatching().ImageSet(m.name, m.images_dir)
					d[m.image_set.get_matches(img,check_homogenity=False)[1]] = m
			r =  d[max(d.keys())]
			print r.code, r.name, 'found'
			return r
		else:
			return None
			
