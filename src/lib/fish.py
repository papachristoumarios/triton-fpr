class Fish:
	"""Stores info for each fish"""
	def __init__(self, name, bodycascade, fcscascades = [], cHL=None, cFL=None, cSL=None): #TODO Add stage/age
		self.name = name; self.bodycascade = cascade
		self.fcascades = fcascades
		self.morphometrics = Morphometrics(cHL, cFL, cSL)
		
	def __str__(self):
		return self.name
			
class Morphometrics(Fish):
	"""Morphometrics are stored at this class"""
	def __init__(self, cHL, cFL, cSL):
		self.cHL, self.cFL, cSL =  cHL, cFL, cSL
		self.names =   {'Head Length' : self.cHL,
						'Fork Length' : self.cFL,
						'Standard Length': self.cSL}
							
	def __str__(self):
		if (self.cHL, self.cFL, self.cSL) is (None,None,None):
			raise Exception('Morphometrics are not defined properly (or they are undefined)')
			return None
		S = ''''''
		for k in self.names.keys():
			s = '{0} Coefficient: {1}% TL \n'.format(k, 100*self.names[k])
			S = S + s
		return S
			
	def print_morphometrics(self):
		print str(self)
		
	def query(artifact,base):
		for f in base:
			if f.name is artifact:
				return f.name + '\n' + str(f.morphometrics) + '\n'		

class Database:
	"""Handle databases (SQL/PostgreSQL)"""
	def __init__(self, name,user):
		#import sqlite3 as db
		#PostgreSQL
		
		import psycopg2 as db
		self.connection = db.connect('dbname='+ filename + ' user=' + user)
		self.name = name
		self.cursor = self.connection.cursor()
		self.tables = []
		
	def execute(self, cmd):
		self.cursor.execute(cmd)
	
class FishDatabase(Database):
	"""Database for fishes"""	
	def __init__(self, imembers=[], name='testdb', user='testuser'):
		self.members = [] + imembers
		#super(Database, self).__init__(name, user)
	
	def append_member(self, m):
		self.members.append(m)
		

