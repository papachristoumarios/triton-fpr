class Fish:

	def __init__(self, name, bodycascade, fcscascades = []):
		self.name = name; self.bodycascade = cascade
		self.fcascades = fcascades
		
	def __str__(self):
		return self.name
	
class FishDatabase(Database):
	
	def __init__(self, imembers=[]):
		self.members = [] + imembers
		#super(Database, self).__init__(self.__name__)
	
	def append_member(self, m):
		self.members.append(m)


class Database:
	
	def __init__(self, filename):
		import sqlite3 as db
		self.connection = db.connect(filename)
		self.filename = filename
		self.cursor = self.connection.cursor()
		self.tables = []
		
	def execute(self, cmd):
		self.cursor.execute(cmd)
			
#class Table:
#	def __init__(self,statement, c):
#		c.execute('CREATE TABLE ' + statement)		
#	def getData(self, keyword):
		
