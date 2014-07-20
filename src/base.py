#BASE FILE
#General Imports needed for main.py to function properly

#Built-in
import os
import sys
import platform
from math import sqrt
import Image

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
#scripts package
import scripts.detector as detector
import scripts.identifier as identifier
#gui
import lib.ui.main_gui as main_gui
#cli
import lib.cli.main_cli as main_cli

def initialize_fishbase():
	global fishbase
	fishbase = fish.FishDatabase()
	#fish_a = ...
	#fish_b = ...
	#fishbase.append_member(fish_a)
	#fishbase.append_member(fish_b)
	#TODO Add some fish
	
initialize_fishbase()
	
	
	
	
