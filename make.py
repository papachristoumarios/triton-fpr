#!/usr/bin/env python2.7

import os,sys,glob,platform, Image
global SRC,LIB,SCRIPTS,CC,CFLAGS, TRASH_FILE_EXT, UI, CLI, DIRECTORIES

TRASH_FILE_EXT=['.pyc','.c','.so']


SRC='src'
LIB='src/lib'
UI='src/lib/ui'
CLI='src/lib/cli'
SCRIPTS='src/scripts'


DIRECTORIES=[SRC,LIB,UI,CLI,SCRIPTS]


CC=['gcc','i586-mingw32msvc-gcc']


CFLAGS='-shared -pthread -fPIC -fwrapv -O2 -Wall -I /usr/include/python2.7' 


def cythonize():
	def _cythonize(_dir):
		os.system('cython {0}/*.py'.format(_dir))
	for d in DIRECTORIES:
		_cythonize(d)
		print 'Cycy!'
	
def clean():
	def _clean(_dir):
		for t in TRASH_FILE_EXT:
			os.system('rm {0}/*{1}'.format(_dir,t))
	for d in DIRECTORIES:
		_clean(d)
		
def gen_so(WINDOWS=False):
	if WINDOWS:
		n=1
	else:
		n=0
		
	def _gen_so(_dir):
		Cfiles = glob.glob('{0}/*.c'.format(_dir))
		for f in Cfiles:
			f = f[:len(f) - 2] #strip .c
			os.system('{0} {1} -o {2}/{3}.so {2}/{3}.c'.format(CC[n],CFLAGS,_dir,f))
	cythonize()	
	for d in DIRECTORIES:
		_gen_so(_dir)
		
def archive():
	os.system('tar -cvf ../triton-fpr/')
	

if __name__ == '__main__':
	FUNC_DIR = {'cythonize': cythonize,
	'clean': clean,
	'gen_so': gen_so,
	'archive': archive}
	

	FUNC_DIR[sys.argv[1]]()
	
	
	

