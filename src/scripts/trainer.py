#!/usr/bin/env python2.7

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os,sys,platform
import psycopg2 as db
import mergevec


class Trainer:
	
	def __init__(self):
		self.cs_cmd = 'opencv_createsamples'
		self.ht_cmd = 'opencv_traincascade' #opencv_traincascade
		if platform.system() is 'Windows':
			self.cs_cmd += '.exe'
			self.ht_cmd += '.exe'
	
	def tcreate_samples(self,input_filename, output_filename, number, width, height):
		"""Create PS via opencv_createsamples
			E.g.: opencv_createsamples -info marked_positives.info -vec data/positives.vec -num 1000 -w 20 -h 20
			Where:
			i. -num: The number of samples
			ii. -w, -h: The min dimensions of the object"""
		
		os.system('{0} -info {1} -vec {2} -num {3} -w {4} -h {5}'.format(self.cs_cmd, input_filename, output_filename, number, width, height))
		return 1
		
	def thaar_training(self, output_dir, vec_filename, npos, nneg, nstage, malloc, mode, width, height, featureType, bg_filename):
		"""Do a Haar Training 
		opencv_haartraining -data data/cascade.xml -vec data/positives.vec -bg 
		negatives/negatives.info -npos 2890 -nneg 2977 -nstage 20 -mem 1000 -mode ALL -w 20 -h 20"""
		os.system('{0} -data {1} -vec {2} -bg {3} -npos {4} -nneg{5} -nstage {6} -mem {7} -mode {8} -w {9} -h {10} -featureType {11}'.format(self.ht_cmd, output_dir, vec_filename, bg_filename, npos, nneg, nstage, malloc, mode, width, height, featureType))
		return 1	
		
class Interface(BoxLayout):
	
	def connect(self):
		global conn, cursor,trainer
		trainer = Trainer()
		_durl = str(self.ids['datasource_input'].text)
		try:
			conn = db.connect(_durl)
			self.ids['status'].text = 'Status: Connected'
			cursor = conn.cursor()
		except db.OperationalError:
			self.ids['status'].text = 'Status: Error'
			
	def create_samples(self):
		while True:
			try:
				cursor.execute('SELECT * FROM "OPENCV_CREATE_SAMPLES"')
				data = cursor.fetchall()
				break
			except db.InternalError:
				conn.rollback()
				continue
		for e in data:
			trainer.tcreate_samples(e[3], e[2], e[4], e[5], e[6])
			
		self.ids['status'].text = 'Status: Samples Created' 	
		return 1
			
	def haar_training(self):
		while True:
			try:
				cursor.execute('SELECT * FROM "OPENCV_HAARTRAINING_TABLE"')
				data = cursor.fetchall()
				break
			except db.InternalError:
				conn.rollback()
				continue		
			
		for e in data:
			trainer.thaar_training(e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9], e[11], e[12], e[10])
		
		self.ids['status'].text = 'Status: Training Finished' 	
		return 1
		
class TrainerGUIApp(App):
	"""Trainer app using kivy frontend"""
	def build(self):
		self.title = 'PostgreSQL Integrated Trainer for Haar Training'
		return Interface()
		
		


if __name__ == '__main__':
	TrainerGUIApp().run()
