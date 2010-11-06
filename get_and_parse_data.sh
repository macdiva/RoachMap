#!/usr/bin/bash

curl http://www.nyc.gov/html/doh/downloads/zip/bigapps/dohmh_restaurant-inspections_002.zip \
  > data/dohmh_restaurant-inspections_002.zip
cd data/
unzip dohmh_restaurant-inspections_002.zip
cd ..
cat data/WebExtract.txt | python2.6 roach_parser.py 30 0 > data/binomial_roaches.tsv
