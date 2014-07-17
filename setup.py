#!/usr/bin/python

import os,platform

DEPENDENCIES = ['cv2','cv','kivy','sys','os','platform','numpy','psyscopg2','sqlite3','Image']
PLATFORM = platform.system()
CWD = os.getcwd()

def dependency_check():
	
	for module in DEPENDENCIES:
		try:
			__import__(module)
			print '{0}: Found!'.format(module)
		except ImportError:
			print '{0}: Not Found!\nPlease install {0} and come back again\nExiting...'.format(module)
 			exit()
 
def install():
	if PLATFORM is 'Linux':
		install_Linux()
	elif PLATFORM is 'Windows':
		install_Windows()
	else:
		pass
def install_Linux():
	os.system('sudo cp ../ -avr /opt/ &&')
	os.chdir('/opt/triton-fpr')
	os.system('sudo ln -s main.py /usr/local/bin/triton-fpr.py')
	os.chdir(CWD)
	
def install_Windows():
	pass
	
	

def uninstall():
	pass	
 
if __name__ == '__main__':
	dependency_check()
	install()
	
