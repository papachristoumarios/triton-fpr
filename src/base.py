"""BASE FILE
General Imports needed for main.py in order to function properly"""

#Built-in
import os
import sys
from math import sqrt
import Image
import psycopg2

#Numpy
import numpy as np

#OpenCV
import cv
import cv2

#Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

#Project Libraries
#lib package
import lib.fish as fish
import lib.shape_analyzer as shape_analyzer
import lib.config_parser as config_parser
#gui
import lib.ui.main_gui as main_gui

def initialize_fishbase(datasource_url):
	"""Populates database and returns a FishDatabase object"""
	try:
		fishbase = fish.FishDatabase(datasource_url) 
		print 'Connection Established'
	except psycopg2.OperationalError:
		exit() 
		
	for specimen in fishbase.species_list:
		code = specimen[0]
		name = specimen[1]	
		f = fish.Fish()
		f.code = code
		f.name = name
		f.bodycascade = fishbase.query_cascade(code,'BC')
		f.fcascades = fishbase.query_feature_cascades(code)
		f.morphometrics.cHL = fishbase.query_morphometrics(code, 'HL')
		f.morphometrics.cFL = fishbase.query_morphometrics(code, 'FL')
		f.morphometrics.cSL = fishbase.query_morphometrics(code, 'SL')
		f.morphometrics.cBD = fishbase.query_morphometrics(code, 'BD')
		f.morphometrics.cPaL = fishbase.query_morphometrics(code, 'PaL')
		f.morphometrics.cPdL = fishbase.query_morphometrics(code, 'PdL')
		f.morphometrics.cPpL = fishbase.query_morphometrics(code, 'PpL')
		f.morphometrics.cPpeL = fishbase.query_morphometrics(code, 'PpeL')
		f.morphometrics.cED = fishbase.query_morphometrics(code, 'ED')
		f.morphometrics.cPoL = fishbase.query_morphometrics(code, 'PoL')
		f.morphometrics.cPcL = fishbase.query_morphometrics(code, 'PcL')
		f.images_dir = fishbase.query_images_dir(code)
		fishbase.append_member(f)	

	print 'Elements were sucessfully populated'
	return fishbase
	
def get_temp_dir():
	"""Returns the temp directory (/tmp under Linux, C:\Temp under win)"""
	import platform
	p = platform.system()
	if 'Linux' in p:
		return '/tmp'
	elif 'Windows' in p:
		return '''C:\Temp'''
	else:
		return '/'
