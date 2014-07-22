#!/usr/bin python
#Command Line Application

#general imports
import Image,cv2,sys,platform; import numpy as np

#parent imports
sys.path.append('../..')
import lib.fish as fish
import identifier
import lib.shape_analyzer as shape_analyzer

#global vars

class MainCLIApp:
	
	def show_about(self):
		about_txt = '''Copyright HCMR 2014 - Triton FPR Project
		This project is released under the {add licensing} License
		Author: Marios Papachristou | Contact: mrmarios97@gmail.com'''
		print about_txt
	
	def run(self):	
		print 'Welcome to Triton FPR Project'
		while 1 is 1:
			print '1. Load an Image'
			print '2. Show credits'
			ans = int(raw_input('Select an option: '))
			if ans is 1:
				break 
			elif ans is 2:
				self.show_about()
			else:
				print 'Please enter a valid option'
			
		self.selected_image_filename = raw_input('Select an image: ')
		 
			
		try:
			Image.open(self.selected_image_filename)
			self.selected_image = cv2.imread(self.selected_image_filename)
			self.chanelled_image = cv2.imread(self.selected_image_filename,0)
		except IOError:
			raise Exception('Bad input')
			exit()
				
		while 1 is 1:		
			print '1. Perform spieces identification'
			print '2. Perform shape analysis'
			if ans is 1:
				self.identification_elements = identifier.identify(self.selected_image, fishbase, detectCharacteristics=False)
				#get artifacts
				S = ''''''
				for k in self.identification_elements.keys():
					s = '{0}: {1}\n'.format(k, self.identification_elements[k])
					S = S + s
					del(s)
				print S
				# show_morphometrics():
				for k in identification_elements.keys():
					m = fish.Morphometrics().query(k, fishbase)
					print m
					
				break
			
			elif ans is 2:
				#global selected_image_shape_analyzer
				self.selected_image_shape_analyzer = shape_analyzer.ShapeAnalyzer(chanelled_image)
				self.selected_image_shape_analyzer.print_details()
				self.selected_image_shape_analyzer.draw_extreme_points_lines()
				self.selected_image_shape_analyzer.draw_details()
				_out = raw_input('Select an output folder: ')
				self.selected_image_shape_analyzer.write_steps(_out) #add more
				break				
			else:
				print 'Please enter a valid option'
			
if __name__ == '__main__':
	sys.path.append('../..')
	import base; global fishbase
	fishbase = base.initialize_fishbase()
	
	MainCLIApp().run()
