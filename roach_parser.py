import sys
import csv
import datetime

# Rewritten by Max Shron from code by John Myles White

# ARGV
# ARGV[1] == Window Size
# ARGV[2] == Window End Offset from Today

roachcode = "04M"

window = int(sys.argv[1])
back = int(sys.argv[2])

datestring = "%Y-%m-%d %H:%M:%S"
now = datetime.datetime.now()

#key: zip, value: {restaurant,code}
zipcodes = {}

for data in csv.reader(sys.stdin):
    if data[0] == 'CAMIS': continue
    d = now - datetime.datetime.strptime(data[8],datestring)
    d = d.days
    if window+back > d > back:
       camis = data[0]
       zipcode = data[5]
       code = data[10] 
       zipcodes.setdefault(zipcode,{}).setdefault(camis,[]).append(code)

zipcodes_out = {}

for z in zipcodes:
    total = 0
    roach = 0
    for r in zipcodes[z]:
       total += 1
       if roachcode in zipcodes[z][r]:
          roach += 1
    zipcodes_out[z] = [str(total),str(roach)]

for z,v in zipcodes_out.iteritems():
    print ','.join([z] + v)
