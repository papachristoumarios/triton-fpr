import os,platform
from objectmarker import *


def negatives_preparation(_dir):
	filelist = os.listdir(_dir)
	with open(_dir + 'negatives.txt', 'w') as f:
		for s in filelist:
			f.write(_dir + s)
		
def vector_file_creation(output_filename,positives_dir ,number, width, height):
	if platform.system() is 'Linux':
		cmd = 'opencv_createsamples'
	else:
		cmd = 'opencv_createsamples.exe'
		
	cmd = '{0} -info {1}/positives.txt -vec {2} -num {3} -w {4} -h {5}'.format(cmd, positives_dir, output_filename, number, width, height)
	os.system(cmd)
		
def haar_training(output_filename, vec_dir, negatives_dir, number_of_positives, number_of_negatives, number_of_stages, malloc, mode, width, height):
	if platform.system() is 'Linux':
		cmd = 'opencv_haartraining'
	else:
		cmd = 'opencv_haartraining.exe'
	
	cmd = '{0} -data {1} -vec {2} -bg {3} -npos {4} -nneg {5} -nstage {6} -mem {7} -mode {8} -w {9} -h {10}'.format(output_filename, vec_dir, negatives_dir, number_of_positives, number_of_negatives, number_of_stages, malloc, mode, width, height)	
	os.system(cmd)

class TrainerAppCLI:

	def run(self):
		print '''This is the trainer script for fish pattern recognition. It generates .xml cascade files
		Steps:
		1. Negatives Preparation
		2. Positives Preparation & Object Marking
		3. Vector file creation
		4. Haar Training \n \n 
		'''
		#STEP 1
		print 'STEP 1: Negatives Preparation'
		_pdir = raw_input('Enter the directory of the negative files: ')
		if not(_ndir.endswith('/')):
			_ndir += '/'
		negatives_preparation(_ndir)
		print 'Done'
		#STEP 2
		print 'STEP 2: Positives Preparation & Object Marking'
		_pdir = raw_input('Enter the directory of the positive files: ')
		_ext = raw_input('Enter image extension (with dot): ')
		if not(_pdir.endswith('/')):
			_pdir += '/'
		table_file_name      = 'positives.txt'
		background_file_name = 'dump.txt'
		image_file_glob      = _pdir + '*' + _ext
		read_rect_table()
		object_detection()
		print 'Done'
		#STEP 3 
		vec_filename = raw_input('Enter the output filename of the .vec file: ')
		number = raw_input('Enter the number of samples: ')
		width = raw_input('Enter minimum width: ')
		height = raw_input('Enter minimum height: ')
		vector_file_creation(vec_filename, _pdir, number, width, height)
		print 'Done'
		#STEP 4
		output_filename = raw_input('Enter the output filename of the cascade .xml file: ')
		M = raw_input('Enter the number of positives, then the number of negatives and the number of stages separated by a comma: ')
		number_of_positives, number_of_negatives, number_of_stages = M.split(',')
		malloc = raw_input('How much memory would you like to allocate for the process?: ')
		haar_training(output_filename, vec_filename, _ndir, number_of_positives, number_of_negatives, number_of_stages, malloc, width, height)
		print 'Done'


class Interface:
	pass
	
class HaarDialog:
	pass 
	
class ObjMarkingDialog:
	pass
	
class NegativesDialog:
	pass 
	
	
	
class TrainerAppGUI(App):
	
	def build(self):
		return Interface()
		
		
	
		
		
if __name__ == '__main__':
	ans = raw_input('Use a graphical user interface? [y/n] :')
	if ans is 'n':
		TrainerAppCLI().run()
	else:
		#kivy imports 
	
	
