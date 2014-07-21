#!/usr/bin/python

from base import *

COMMAND_LINE_APP = False
BANNER = '../../res/logo/bitmap/banner_90dpi.png'

if __name__ == '__main__':
	#if sys.argv[1] is '--cli':
	#	COMMAND_LINE_APP = True
	
	
	if COMMAND_LINE_APP is False:
		main_gui.MainGUIApp().run()
	else:
		main_cli.MainCLIApp().run()
