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
import re
from datetime import *

window_size = int(sys.argv[1])
window_end = int(sys.argv[2])

input = csv.reader(sys.stdin)

total_inspections = {}
roach_findings = {}

for row in input:
    try:
        incident_dba = row[1]
        incident_zipcode = row[5]
        incident_timestamp = row[8]
        incident_violation_code = row[10]
        incident_datetime = datetime.strptime(incident_timestamp, '%Y-%m-%d %H:%M:%S')
        temporal_distance = date.today()- incident_datetime.date()
        if temporal_distance <= timedelta(window_size + window_end) and temporal_distance >= timedelta(window_end):
            if total_inspections.has_key(incident_zipcode):
                total_inspections[incident_zipcode] = total_inspections[incident_zipcode] + 1
            else:
                total_inspections[incident_zipcode] = 1
            if incident_violation_code == '04M':
                if roach_findings.has_key(incident_zipcode):
                    roach_findings[incident_zipcode] = roach_findings[incident_zipcode] + 1
                else:
                    roach_findings[incident_zipcode] = 1
    except:
        1 # We're just ignoring errors for time being.

for zipcode in total_inspections.keys():
    if not re.search(r'\d{5}', zipcode):
        continue
    if not roach_findings.has_key(zipcode):
        roach_findings[zipcode] = 0
    print "\t".join([zipcode, str(total_inspections[zipcode]), str(roach_findings[zipcode])])
