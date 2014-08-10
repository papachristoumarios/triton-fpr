#!/usr/bin/env python2.7

#general imports
import Image,cv2,sys,time; import numpy as np

#kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

#parent imports
sys.path.append('../..')
import lib.shape_analyzer as shape_analyzer
import lib.config_parser as config_parser

#global vars
global selected_image_filename,fishbase

class LoadDialog(BoxLayout):
	"""Load dialog"""
	def load(self):
		"""Loads defined image"""
		global selected_image,chanelled_image
		selected_image_filename = self.ids['load_filechooser'].selection[0]
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
		
	def get_home(self):
		import os; return os.getenv('HOME')
		
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
		return 'Species: {0} HCMR Code: {1}'.format(identified_specimen.name, identified_specimen.code)
		
	def show_morphometrics(self):
		self.ids['output_label'].text +=  ('\n' + str(identified_specimen.get_morphometrics()))
	
	def close(self):
		identifier_interface_popup.dismiss()
			
class ShapeAnalyzerInterface(BoxLayout):
	
	def close(self):
		shape_analyzer_popup.dismiss()
		
	def refresh(self):
		self.ids['shape_analyzed_image'].reload()
		
	def draw_el(self):
		selected_image_shape_analyzer.draw_extreme_points_lines()
		selected_image_shape_analyzer.write_final_image(TEMP_DIR)
		self.refresh()
		
	def draw_ml(self):
		selected_image_shape_analyzer.draw_morphometric_lines_according_to_specimen(identified_specimen)
		selected_image_shape_analyzer.write_final_image(TEMP_DIR)
		#EOE
		self.refresh()
				
class Interface(BoxLayout):
	"""Class that handles the main interface"""
	
	def get_banner(self):
		return BANNER
				
	def show_load(self):
		global load_popup
		load_popup = Popup(title='Load an Image',
		content=LoadDialog(),
		size_hint=(None, None), size=(600, 600))
		load_popup.open()
			
	def show_about_dialog(self):
		global about_dialog_popup
		about_dialog_popup = Popup(title= 'About',
		content = AboutDialog(),
		size_hint=(None,None), size=(500,500))
		about_dialog_popup.open()
		
	def perform_identification(self):
		global identified_specimen
		identified_specimen = fishbase.identify(chanelled_image)
		
	def perform_identification2(self):
		_t = time.time()
		global identified_specimen
		try:
			identified_specimen = fishbase.identify2(chanelled_image)
			_dt = time.time() - _t
		except NameError:
			print 'Specimen is not defined!'
			return
		global identifier_interface_popup
		identifier_interface_popup = Popup(title= 'Identified specimen. Identification time: {0} sec'.format(_dt),
		content = IdentifierInterface(),
		size_hint=(None,None), size=(600,800))
		identifier_interface_popup.open()
			
	def perform_shape_analysis(self):
		global selected_image_shape_analyzer
		_threshold1 = int(self.ids['sl1'].value)
		_threshold2 = int(self.ids['sl2'].value)
		selected_image_shape_analyzer = shape_analyzer.ShapeAnalyzer(chanelled_image,threshold1=_threshold1, threshold2=_threshold2)
		selected_image_shape_analyzer.write_final_image(TEMP_DIR)
		global shape_analyzer_popup
		shape_analyzer_popup = Popup(title= 'Shape Analyzer',
		content = ShapeAnalyzerInterface(),
		size_hint=(None,None), size=(700,700))
		shape_analyzer_popup.open()
		
	def clear_all(self):
		"""Clears all the defined parameters"""
		identified_specimen = None
		selected_image = None
		selected_image_filename = None
		selected_image_shape_analyzer = None
		chanelled_image = None
		print 'Cleared'

class MainGUIApp(App):
	"""Main GUI Application"""

	def build(self):
		self.title = 'Triton FPR'
		return Interface()

	def _setup(self,fb, banner, tmp_dir='/tmp'):
		"""Sets up global parameters"""
		global fishbase, BANNER, TEMP_DIR
		fishbase = fb
		BANNER = banner
		TEMP_DIR = tmp_dir

if __name__ == '__main__':
	"""Executed if standalone"""
	#general imports
	sys.path.append('../..')
	import base
	
	#configurations
	conf_parser = config_parser.ConfigParser('../../config.spec',regex=':')
	fishbase = base.initialize_fishbase(conf_parser.get('DATASOURCE_URL'))
	banner = '../../../res/logo/bitmap/banner_90dpi.png'
	tmp_dir = base.get_temp_dir()
	
	#execution
	main_gui_app = MainGUIApp()
	main_gui_app._setup(fishbase, banner, tmp_dir)
	main_gui_app.run()
