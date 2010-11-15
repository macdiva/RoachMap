'''Usage: draw_map.py [input.tsv] -> roachmap-[date].png'''
from __future__ import division
import numpy as np
import matplotlib as ma
ma.use('agg')
import matplotlib.pyplot as plt
import cPickle as cp
import sys
import datetime
import json

def colorfunc(v,x):
#  v = np.sort(v)
#  spot = np.flatnonzero(x<v)[0]
  spot = np.interp(x,[np.min(v),np.max(v)],[0,1])
  #quintile
  spot = int(spot*5)
  spot = spot/5
#spot /= float(len(v))
  spot_r = np.interp(spot,[0,1],[.99,.7])
  spot_gb = np.interp(spot,[0,1],[.8,0])
  colormap = [[1,1,1],
              [.8,0,0]]
  return (spot_r,spot_gb,spot_gb)

map_projected = cp.load(open('zip_projected.pkl'))
zip_values_file = open(sys.argv[1])

zip_values = {}

for line in zip_values_file:
  data = line.strip().split(',')
  zip_values[data[0]] = (float(data[2]),float(data[1]))

#beta prior, binomial data
z_values = np.asarray(zip_values.values())
z_bin_means = (z_values[:,0]+.5)/(z_values[:,1]+.5)
m = np.mean(z_bin_means)
v = np.var(z_bin_means)
alpha = m*((m/v)*(1-m) - 1)
beta = (1-m)*((m/v)*(1-m) - 1)


zip_values_adjusted = {}
for z,v in zip_values.iteritems():
  zip_values_adjusted[z] = (alpha+v[0])/(alpha+beta+v[1])
plt.figure()
ax = plt.gca()

for z,l in map_projected.items():
  try:
    facecolor = colorfunc(zip_values_adjusted.values(),zip_values_adjusted[z])
    edgecolor = [max(x-.1,0) for x in facecolor]
  except:
    facecolor = (.9,.9,.9)
    edgecolor = (.95,.95,.95)
  for p in l:
    ax.add_patch(ma.patches.Polygon(p,fc=facecolor, ec=edgecolor))
    plt.plot(p[:,0],p[:,1],c=edgecolor,alpha=.5,lw=.001)

bincounts = np.histogram(zip_values_adjusted.values(),5)

for i in xrange(5):
  xy = [np.interp(i,[0,5],[.15,.4]),.7]
  c_r = np.interp(i,[0,4],[.99,.7])
  c_gb = np.interp(i,[0,4],[.8,0])
  c = (c_r,c_gb,c_gb)
  h = np.interp(bincounts[0][i],[np.min(bincounts[0]),np.max(bincounts[0])],[0,.1]) + .002
  ax.add_patch(ma.patches.Rectangle(xy,.05,h,color=c,transform=ax.transAxes))

#print json.dumps(zip_values_adjusted)

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

table = open('roachincidence_%s-%s-%s.tsv'%(year,month,day),'w')
out = sorted(zip_values_adjusted.items(),key = lambda x: x[1])
for z,v in out[::-1]:
   if len(z)!=5 or int(z)>20000: # filter out placeholders, only allow NYC
      continue
   roach,total = zip_values[z]
   table.write("%s\t%.02f\t%i\t%i\n"%(z,v,roach,total))

ax.text(.15,.69,"Least",transform=ax.transAxes,va='top')
ax.text(.34,.69,"Most",transform=ax.transAxes,va='top')
ax.text(.15,.65,"fraction of \nrestaurant \ninspections \nthat turned up \ncockroaches \n(sample-size \nadjusted)",transform=ax.transAxes,va='top',fontsize=10)


plt.title("Where are the roaches in the past four weeks?")

footer = "roachmap.com: auto-generated %s-%s-%s from\n nyc.gov/data for the Great Urban Hack 2010. #hacknyc."%(month,day,year)

ax.text(1,0,footer,transform=ax.transAxes,ha='right')

ax.set_frame_on(False)
ax.set_axis_off()

plt.savefig('roachmap_%s-%s-%s.png'%(year,month,day))
