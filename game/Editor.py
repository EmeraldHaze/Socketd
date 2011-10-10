#!/usr/bin/python
#Syntax for use:
#
#spd\<description>
#Changes the current tile's type to 'sp' and adds a sp argument for the __init__: description
#
#set\<type>
#Sets the current tile's type to type
#
#setto\<type>:<decrtiption>
#Sets the current tile's type to type, and adds an entry in the table for that type
#
#tp\<Cord>
#teleports you to cord. Case insestive.


from Maps.TheMap import Main as map
import json
import re

def getdir(place):
      Dir = raw_input('Where do you want to go?  ').upper()
      if Dir not in place.dirlinks:
            p('Please give a good direction')
            Dir = getdir(place)
      return Dir

def getCordLine(cord):
    """The descriptions start at line 25, with A1. Then it goes B1, etc. Basicly interpret this is as a base-<map length> number, with the numebr the 'tens' and the letter the 'ones'. Ha. A1 should be 24+1+(1-1)*8 (on a 8x8 map), C4 will be 24+3+(4-1)*8, etc."""
    line = 24
    lttr = ord(cord[0]) - ord('A') + 1
    num = int(cord[1])-1
    base = map.l
    return line+lttr+num*base

###Parsers:
def set(line,  given):
    typestart = line.find('\'')
    typeend = line.find('\'',  typestart+1)#Compensate for index diffrence
    return line[:typestart+1]+given+line[typeend:]

def spd(line,  given):
    line = set(line,  'sp')
    return line[:-2]+', sp = "'+given+ '")\n'

def setto(line,  given):
    given = given.split(':')
    key = given[0]
    value = given[1]
    #Mini-parse
    tablette = ''.join(open('Maps/TheMap/Types.py',  'r').readlines()[1:])
    table = json.loads(tablette)
    #Get the thing we're updating
    table[key] = value
    #Update it
    types = open('Maps/TheMap/Types.py',  'w')
    types.write('types =\\\n'+json.dumps(table).replace('", ',  '",\n'))
    types.close()
    line = set(line,  key)
    return line

def view(line,  view):
    print line,
    return line

parsers = {'set':set,  'spd':spd,  'setto':setto,  'view':view}
##Adding parsers only requiers you to define it and add it to the list


print map.story
currentCord = map.startt
place = getattr(map, map.startt)

while True:
    print 'Cords: '+currentCord
    look = place.look+' Exits: '
    for Dir in place.dirlinks:
        look+=Dir+', '
        look = look[:-2]
    print look
    if place.end == True:
        break

    ###Parse
    action = raw_input('What do you want to do?   ')
    if len(action) == 1:
        newdir = action
        i = place.dirlinks.index(newdir.upper())
        currentCord = place.cordlinks[i]
    elif action[:3] == 'tp ':
        currentCord  = action[3:].upper()
    elif action == '':
        pass
    else:
        action = re.split('\\\\|:|/| ', action,  1)
        action.append('Dummy')#For no-arg commands. That way, there is always a action[1]
        lines = open('Maps/TheMap/Main.py').readlines()
        line = getCordLine(currentCord)-1#getCordLine indexs form 1, we index from 0
        lines[line] = parsers[action[0]](lines[line],  action[1])
        newmap = ''.join(lines)
        Pin = open('Maps/TheMap/Main.py',  'w')
        Pin.write(newmap)
        Pin.close()


    place = getattr(map, currentCord)
print 'You win! Congrats. Now refresh to play again, we don\'t support play again yet.'
