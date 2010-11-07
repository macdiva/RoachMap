#!/usr/bin/python2.6

import system
import os
from datetime import *

os.chdir('/home/roachmap/backend')

date_string = date.today().strftime('%Y-%m-%d')
os.system('mv data data_' + date_string)
os.system('mkdir data')

data_mine_url = 'http://www.nyc.gov/html/doh/downloads/zip/bigapps/dohmh_restaurant-inspections_002.zip'

os.system('curl ' + data_mine_url + ' > data/dohmh_restaurant-inspections_002.zip')

os.chdir('data')
os.system('unzip dohmh_restaurant-inspections_002.zip')
os.chdir('..')

os.system('cat data/WebExtract.txt | python2.6 roach_parser.py 90 0 > data/binomial_roaches.tsv')

