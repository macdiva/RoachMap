from __future__ import division
import numpy as np
import matplotlib as ma
ma.use('agg')
import matplotlib.pyplot as plt
import cPickle as cp
import sys

def colorfunc(x):
  return (1-x,0,0)

map_projected = cp.load(open('zip_projected.pkl'))
zip_restaurants_file = open(sys.argv[1])

zip_restaurants = {}

for line in zip_restaurants_file:
  data = line.strip().split()
  zip_restaurants.setdefault(data[0],[]).append(data[1])

zip_values = {}
top = 50
for z,r in zip_restaurants.iteritems():
  zip_values[z] = len(r)/top

rotation = ma.transforms.Affine2D().rotate(.2)

plt.figure()
ax = plt.gca()
for z,l in map_projected.items():
  try:
    facecolor = colorfunc(zip_values[z])
    edgecolor = [max(x-.1,0) for x in facecolor]
  except: 
    facecolor = (.9,.9,.9)
    edgecolor = (.95,.95,.95)
  for p in l:
    ax.add_patch(ma.patches.Polygon(p,fc=facecolor, ec=edgecolor))
    plt.plot(p[:,0],p[:,1],c=edgecolor,alpha=.5,lw=.01)

ax.set_frame_on(False)
ax.set_axis_off()


plt.savefig('test.png')
