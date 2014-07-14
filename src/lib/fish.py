class Fish:

	def __init__(self, name, bodycascade, fcscascades = []):
		self.name = name; self.bodycascade = cascade
		self.fcascades = fcascades
		
	def __str__(self):
		return self.name

class Database:
	pass 
	
class FishDatabase(Database):
	
	def __init__(self, imembers=[]):
		self.members = [] + imembers
	
	def append_member(self, m):
		self.members.append(m)
