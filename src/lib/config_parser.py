class ConfigParserException(Exception):
	pass

class ConfigParser:
	"""Parses configuration files"""
	def __init__(self, filename,regex='='):
		self.filename = filename
		self.regex = regex
		self.things = {}
		with open(filename, 'r') as f:
			lines = f.readlines()
		for line in lines:
			line = line.split(regex)
			self.things[line[0]] = line[1]
			
	def get(self,p):
		try:
			return self.things[p]
		except KeyError:
			raise ConfigParserException()
			
	def append(self, p, v):
		self.things[p] = v

	def rewrite(self):
		with open(self.filename, 'w') as f:
			for k in self.things.keys():
				f.write('{0}={1}'.format(k,self.things[k]))
