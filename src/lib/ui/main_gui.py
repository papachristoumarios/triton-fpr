#general imports
import Image,cv2,sys,platform; import numpy as np

#kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

#parent imports
sys.path.append('../..')
import lib.fish as fish
import identifier
import lib.shape_analyzer as shape_analyzer

#global vars
global selected_image_filename


class LoadDialog(BoxLayout):
	"""Load dialog"""
	def load(self):
		"""Loads defined image"""
		global selected_image
		global chanelled_image
		selected_image_filename = self.ids['load_text_input'].text
		try:
			Image.open(selected_image_filename)
			selected_image = cv2.imread(selected_image_filename)
			chanelled_image = cv2.imread(selected_image_filename,0)
			print selected_image_filename + ' loaded'
			load_popup.dismiss()
		except IOError:
			selected_image = None
			raise Exception('Bad Input')
			
	def cancel(self):
		"""Dismisses the popup"""
		load_popup.dismiss()
		
class AboutDialog(BoxLayout):
	
	def get_about_text(self):
		"""Returns the about text"""
		about_txt = '''Copyright HCMR 2014 - Triton FPR Project
This project is released under the {add licensing} License
Author: Marios Papachristou | Contact: mrmarios97@gmail.com'''
		
		return about_txt
		
	def go_to_homepage(self):
		"""Opens homepage via xdg-open"""
		from os import system
		system('xdg-open http://http://www.hcmr.gr/en/')
		
	def close(self):
		"""Closes the popup"""
		about_dialog_popup.dismiss()	
		
class IdentifierInterface(BoxLayout):
	
	def get_artifacts(self):
		S = ''''''
		for k in identification_elements.keys():
			s = '{0}: {1}\n'.format(k, identification_elements[k])
			S = S + s
		del(s)
		return S
		
	def show_morphometrics(self):
		for k in identification_elements.keys():
			m = fish.Morphometrics().query(k, fishbase)
			self.ids['output_label'].text += m
			
class ShapeAnalyzerInterface(BoxLayout):
	
	def close(self):
		shape_analyzer_popup.dismiss()
		
	def refresh(self):
		self.ids['shape_analyzed_image'].reload()
		
	def draw_el(self):
		selected_image_shape_analyzer.draw_extreme_points_lines()
		selected_image_shape_analyzer.write_final_image('/tmp')
		self.refresh()
		
	def draw_ml(self):
		#EXAMPLE! CAUTION DO NOT USE
		
		f1 = fish.Fish('f1',cHL = 0.25, cFL = 0.3, cSL = 0.1)
		selected_image_shape_analyzer.draw_morphometric_lines_according_to_specimen(f1)
		selected_image_shape_analyzer.write_final_image('/tmp')
		#EOE
		self.refresh()
				
class Interface(BoxLayout):
	"""Class that handles the main interface"""
	
	def get_banner(self):
		return '../../../res/logo/bitmap/banner_90dpi.png'

	def foo(self):
		print 'foo'
		
	def show_load(self):
		global load_popup
		load_popup = Popup(title='Load an Image',
		content=LoadDialog(),
		size_hint=(None, None), size=(400, 400))
		load_popup.open()
		
	def show_identifier_interface(self):
		global identifier_interface_popup
		identifier_interface_popup = Popup(title= 'Identifier',
		content=IdentifierInterface(),
		size_hint=(None,None), size=(500,500))
		identifier_interface_popup.open()
	
	def show_about_dialog(self):
		global about_dialog_popup
		about_dialog_popup = Popup(title= 'About',
		content = AboutDialog(),
		size_hint=(None,None), size=(500,500))
		about_dialog_popup.open()
		
	def perform_identification(self):
		global identification_elements
		identification_elements = identifier.identify(selected_image, fishbase, detectCharacteristics=False)
		
	def perform_shape_analysis(self):
		global selected_image_shape_analyzer
		selected_image_shape_analyzer = shape_analyzer.ShapeAnalyzer(chanelled_image)
		selected_image_shape_analyzer.write_final_image('/tmp')
		global shape_analyzer_popup
		shape_analyzer_popup = Popup(title= 'Shape Analyzer',
		content = ShapeAnalyzerInterface(),
		size_hint=(None,None), size=(800,800))
		shape_analyzer_popup.open()
		
	def clear_all(self):
		identification_elements = None
		selected_image = None
		selected_image_filename = None
		selected_image_shape_analyzer = None
		print 'Cleared'

class MainGUIApp(App):

	def build(self):
		self.title = 'Triton FPR'
		return Interface()

if __name__ == '__main__':
	#general imports
	sys.path.append('../..')
	from base import *
	MainGUIApp().run()
