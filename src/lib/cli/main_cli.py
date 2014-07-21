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
global selected_image_filename


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
			selected_image_filename = raw_input('Select an image: ')
			global selected_image; global chanelled_image 
			
		try:
			Image.open(selected_image_filename)
			selected_image = cv2.imread(selected_image_filename)
			chanelled_image = cv2.imread(selected_image_filename,0)
		except IOError:
			raise Exception('Bad input')
			exit()
				
		while 1 is 1:		
			print '1. Perform spieces identification'
			print '2. Perform shape analysis'
			if ans is 1:
				global identification_elements
				identification_elements = identifier.identify(selected_image, fishbase, detectCharacteristics=False)
				def get_artifacts():
					S = ''''''
					for k in identification_elements.keys():
						s = '{0}: {1}\n'.format(k, identification_elements[k])
						S = S + s
						del(s)
					print S
				get_artifacts()

				def show_morphometrics():
					for k in identification_elements.keys():
						m = fish.Morphometrics().query(k, fishbase)
						print m
						
				show_morphometrics()
				break
			
			elif ans is 2:
				global selected_image_shape_analyzer
				selected_image_shape_analyzer = shape_analyzer.ShapeAnalyzer(chanelled_image)
				selected_image_shape_analyzer.print_details()
				selected_image_shape_analyzer.draw_extreme_points_lines()
				selected_image_shape_analyzer.draw_details()
				_out = raw_input('Select an output folder: ')
				selected_image_shape_analyzer.write_steps(_out) #add more
				break				
			else:
				print 'Please enter a valid option'
			
if __name__ == '__main__':
	sys.path.append('../..')
	from base import *
	MainCLIApp().run()
