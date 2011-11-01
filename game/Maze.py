#!/usr/bin/python
from Maps.TheMap import Main as map
import sys, prep
sys.stdout = prep.stdout

place = getattr(map, map.startt)
newcords = map.startt
debug = False

print("The game is very simple. You are trapped in a dungeon. You can use N, S, E, and W to move about it, depending on where you are(Case insensitive). These one-letter commands are the ONLY ones there are. Remember to click on the text box on the bottom of the screen. There are a couple of portals, use them with T. You may die/get trapped, in which case you will be giving but one choice, to T to the starting point. So be careful out there! Note: As of version 1.2, you are unlikly to be eaten by a grue.")
raw_input("Type 'c' to continue")

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
