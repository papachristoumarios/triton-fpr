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

#global vars
global fishbase
global selected_image_filename
global selected_image
fishbase = fish.FishDatabase()

class LoadDialog(BoxLayout):
	"""Load dialog"""
	def load(self):
		"""Loads defined image"""
		selected_image_filename = self.ids['load_text_input'].text
		try:
			Image.open(selected_image_filename)
			selected_image = cv2.imread(selected_image_filename)
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
		about_txt = '''Copyright HCMR 2014 - Triton FPR Project
		This project is released under the {add licensing} License
		Author: Marios Papachristou | Contact: mrmarios97@gmail.com'''
		
		return about_txt
		
	def go_to_homepage(self):
		from os import system
		system('xdg-open http://http://www.hcmr.gr/en/')
		
	def close(self):
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
		
		

class Interface(BoxLayout):
	"""Class that handles the main interface"""
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
	
class MainGUIApp(App):

	def build(self):
		return Interface()

if __name__ == '__main__':
	MainGUIApp().run()
