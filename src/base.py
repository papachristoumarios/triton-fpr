#BASE FILE
#General Imports needed for main.py to function properly

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
import lib.manipulator as manipulator
import lib.shape_analyzer as shape_analyzer
#scripts package
#gui
import lib.ui.main_gui as main_gui
#cli
import lib.cli.main_cli as main_cli

def initialize_fishbase():
	"""Populates database"""
	try:
		fishbase = fish.FishDatabase('dbname=fishbase user=postgres host=localhost password=1997') 
		print 'Connection Established'
	except psycopg2.OperationalError:
		exit() #do sth
		
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
		#print code, name
		fishbase.append_member(f)	

	print 'Elements were sucessfully populated'
	return fishbase
	
def get_temp_dir():
	import platform
	p = platform.system()
	if 'Linux' in p:
		return '/tmp'
	elif 'Windows' in p:
		return 'C:\Temp'
	else:
		return '/'
