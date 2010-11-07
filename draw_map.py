'''Usage: draw_map.py [input.tsv] -> roachmap-[date].png'''
from __future__ import division
import numpy as np
import matplotlib as ma
ma.use('agg')
import matplotlib.pyplot as plt
import cPickle as cp
import sys
import datetime

def colorfunc(v,x):
  v = np.sort(v)
  spot = np.flatnonzero(x<v)[0]
  spot /= float(len(v))
  spot = np.interp(spot,[0,1],[.99,.3])
  return (spot,0,0)

map_projected = cp.load(open('zip_projected.pkl'))
zip_values_file = open(sys.argv[1])

zip_values = {}

for line in zip_values_file:
  data = line.strip().split()
  zip_values[data[0]] = (float(data[2]),float(data[1]))

#beta prior, binomial data
z_values = np.asarray(zip_values.values())
z_bin_means = (z_values[:,0]+.5)/(z_values[:,1]+.5)
m = np.mean(z_bin_means)
v = np.var(z_bin_means)
alpha = m*((m/v)*(1-m) - 1)
beta = (1-m)*((m/v)*(1-m) - 1)

for z,v in zip_values.iteritems():
  zip_values[z] = (alpha+v[0])/(alpha+beta+v[1])
plt.figure()
ax = plt.gca()

for z,l in map_projected.items():
  try:
    facecolor = colorfunc(zip_values.values(),zip_values[z])
    edgecolor = [max(x-.1,0) for x in facecolor]
  except:
    facecolor = (.9,.9,.9)
    edgecolor = (.95,.95,.95)
  for p in l:
    ax.add_patch(ma.patches.Polygon(p,fc=facecolor, ec=edgecolor))
    plt.plot(p[:,0],p[:,1],c=edgecolor,alpha=.5,lw=.01)

for i in xrange(5):
  xy = [np.interp(i,[0,5],[.15,.4]),.7]
  c = (np.interp(i,[0,5],[.99,.3]),0,0)
  ax.add_patch(ma.patches.Rectangle(xy,.05,.05,color=c,transform=ax.transAxes))

ax.text(.15,.69,"Low %",transform=ax.transAxes,va='top')
ax.text(.35,.69,"High",transform=ax.transAxes,va='top')
plt.title("Where are the roaches in the past four weeks?")

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

footer = "roachmap.com: auto-generated %s-%s-%s from\n nyc.gov/data for the Great Urban Hack 2010. #hacknyc."%(month,day,year)

ax.text(1,0,footer,transform=ax.transAxes,ha='right')

ax.set_frame_on(False)
ax.set_axis_off()


plt.savefig('archive/roachmap_%s-%s-%s.png'%(year,month,day))
plt.savefig('roachmap.png')
