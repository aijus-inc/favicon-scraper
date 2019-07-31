# main.py

import requests
import json
import urllib
from bs4 import BeautifulSoup
import const
import func
import sys

opt = ''

if len(sys.argv) > 1:
	opt = sys.argv[1]

if opt == 'reset':
	#reset companys data for test
	print('Is this command for test environment? (y/n)')
	input_chara = raw_input('>>>  ')
	if input_chara == 'y':
		func.reset_all_companies()
	else:
		print('canceled')
elif opt == 'favicon':
	func.get_all_favicons()
elif opt == 'show':
	func.show_companys()
elif opt == 'test':
	func.test()
else:
	# main process
	print('start main')
	func.get_all_address()

print('finish_all')
