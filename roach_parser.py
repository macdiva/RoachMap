#!/usr/bin/python2.6

# RoachMap backend parser
# John Myles White
# 11/6/2010

# ARGV
# ARGV[1] == Window Size
# ARGV[2] == Window End Offset from Today

# Pass in an integer, which is the number of days before now during
# which incidents are counted.

# Loops over lines, only considers lines with VIOLCODE == '04M'
# Outputs a tab-separated file with zipcodes and DBA.

import sys
import csv
from datetime import *

window_size = int(sys.argv[1])
window_end = int(sys.argv[2])

input = csv.reader(sys.stdin)

for row in input:
    try:
        incident_dba = row[1]
        incident_zipcode = row[5]
        incident_timestamp = row[8]
        incident_violation_code = row[10]
        if incident_violation_code != '04M':
            continue
        else:
            incident_datetime = datetime.strptime(incident_timestamp, '%Y-%m-%d %H:%M:%S')
            temporal_distance = date.today()- incident_datetime.date()
            if temporal_distance <= timedelta(window_size + window_end) and temporal_distance >= timedelta(window_end):
                print "\t".join([incident_zipcode, incident_dba])
    except:
        1 # We're ignoring errors for time being.
