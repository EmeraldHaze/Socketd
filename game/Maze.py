#!/usr/bin/python
from Maps.TheMap import Main as map
import sys, prep
sys.stdout = prep.stdout

place = getattr(map, map.startt)
newcords = map.startt
debug = True

def getdir(place):
      Dir = raw_input('Where do you want to go?  ').upper()
      if Dir not in place.dirlinks:
            print 'Please give a good direction'
            Dir = getdir(place)
      return Dir

print map.story

while True:
    if debug == True:
        print newcords

    look = place.look+' Exits: '
    for Dir in place.dirlinks:
        look+=Dir+', '
        look = look[:-2]
    print look
    if place.end == True:
        break
    newdir = getdir(place)
    i = place.dirlinks.index(newdir)
    newcords = place.cordlinks[i]
    place = getattr(map, newcords)

print 'You win! Congrats. Now refresh to play again, we don\'t support play again yet.'
