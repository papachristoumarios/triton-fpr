class Fish:
	"""Stores info for each fish"""
	def __init__(self, name='', bodycascade=None, fcascades = [], cHL=None, cFL=None, cSL=None): #TODO Add stage/age
		self.name = name; self.bodycascade = bodycascade;
		self.fcascades = fcascades
		self.morphometrics = Morphometrics(cHL, cFL, cSL)
		self.code = None
		
	def __str__(self):
		return self.name
			
class Morphometrics(Fish):
	"""Morphometrics are stored at this class"""
	def __init__(self, cHL, cFL, cSL):
		self.cHL, self.cFL, self.cSL =  cHL, cFL, cSL
		self.names =   {'Head Length' : self.cHL,
						'Fork Length' : self.cFL,
						'Standard Length': self.cSL}
							
	def __str__(self):
		if (self.cHL, self.cFL, self.cSL) is (None,None,None):
			raise Exception('Morphometrics are not defined properly (or they are undefined)')
			return None
		S = ''''''
		for k in self.names.keys():
			s = '{0} Coefficient: {1}/100 of TL \n'.format(k, 100*self.names[k])
			S = S + s
		return S
			
	def print_morphometrics(self):
		print str(self)
		
	def query(artifact,base):
		for f in base:
			if f.name is artifact:
				return f.name + '\n' + str(f.morphometrics) + '\n'		

class DatabaseConnection:
	pass

class Database(DatabaseConnection):
	"""Handle databases (SQL/PostgreSQL)"""
	def __init__(self, datasource_url): 	
		import psycopg2 
		self.connection = psycopg2.connect(datasource_url)
		self.cursor = self.connection.cursor()
		
	def execute(self, cmd):
		self.cursor.execute(cmd)
	
	def query(self,q):
		self.cursor.execute(q)
		return self.cursor.fetchall()


#DELETE?
class Table(Database):
	def __init__(self,name,fields,datatypes):
		self.name, self.fields, self.datatypes = name, fields, datatypes
		cmd = 'CREATE TABLE {0} (\n'.format(name)
		for i in xrange(len(fields)):
			cmd = cmd + '{0} {1}'.format(fields[i],datatypes[i])
		cmd = cmd + ')'
		super(Database, self).execute(cmd)	
	
	def __del__(self):
		cmd = 'DROP TABLE {0};'.format(self.name)
		super(Database, self).execute(cmd)
	
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
		
	def get_members_as_string(self):
		"""Returns a string containing all the members"""
		s = []
		for m in self.members:
			s.append(str(m))
		return s
		
	def query_morphometrics(self, code, morph):
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
		r = self.db.query('''SELECT * FROM "CASCADE_MASTER" WHERE "CD_SPECIES"='{0}' AND "CD_CASCADE"='{1}'; '''.format(code,casc))
		if len(r) is 0:
			return None
		else:
			return r[0][2]
			
	def query_feature_cascades(self, code): #feature cascade class?
		r = self.db.query('''SELECT * FROM "CASCADE_MASTER" WHERE "CD_SPECIES"='{0}' AND "CD_CASCADE"!='BC';'''.format(code))
		features = []
		if len(r) is 0:
			return [()]
		else:
			for e in r:
				features.append(r[1:])
			return features #returns feature name, xml-dir
		
			
	def query_code(self, code, name=False):
		for m in self.members:
			if m.code is code:
				if name:
					return m.name
				return m
		return None

	#open image in 0 mode
	def identify(self,img, draw=False, detectCharacteristics=False):
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
		
		
