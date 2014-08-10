#!/usr/bin/python
"""Main Application"""

from base import *

if __name__ == '__main__':
	#configurations
	conf_parser = config_parser.ConfigParser('config.spec',regex=':')
	global fishbase
	fishbase = initialize_fishbase(conf_parser.get('DATASOURCE_URL'))
	banner = '../res/logo/bitmap/banner_90dpi.png'
	
	#run
	main_gui_app = main_gui.MainGUIApp()
	main_gui_app._setup(fishbase, banner, get_temp_dir())
	main_gui_app.run()
