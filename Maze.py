#!/usr/bin/python
from Maps.TheMap import Main as map
import sys
sys.path.append('/home/glycan/Documents/Python/Converter')
from prep import *
#def p(s):
#    print s
place = getattr(map, map.startt)
debug = False
def getdir(place):
      Dir = raw_input('Where do you want to go?  ').upper()
      if Dir not in place.dirlinks:
            p('Please give a good direction')
            Dir = getdir(place)
      return Dir
p(map.story)
while True:
    try:
        if debug == True:
            p(newcords)
    except:
        pass

    look = place.look+' Exits: '
    for Dir in place.dirlinks:
        look+=Dir+', '
        look = look[:-2]
    p(look)
    if place.end == True:
        break
    newdir = getdir(place)
    i = place.dirlinks.index(newdir)
    newcords = place.cordlinks[i]
    place = getattr(map, newcords)

print 'You win! Congrats. Now refresh to play again, we don\'t support play again yet.'
