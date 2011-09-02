def switch(a, b):
      return chr(a)+str(b)

fn = raw_input('Filename? [No extention]\n')+'.py'
n = input('Mapsize? [NxN]\n')
f = open(fn, 'w')
cordtable = {'N': lambda x, y: switch(x, y-1), 'S': lambda x, y: switch(x, y+1), 'E': lambda x, y: switch(x+1, y), 'W': lambda x, y: switch(x-1, y)}
startt = raw_input('Starting tile?\n')
f.write('startt = '+startt)
f.write("""
types = {'Hall': 'A hall.',
}
class Place:
        def __init__(self, Type, dirlinks, cordlinks, **kwargs):
                self.cordlinks = cordlinks
                self.dirlinks = dirlinks
                if Type == 'sp':
                        self.look = kwargs['sp']
                else:
                        self.look = types[Type]
                self.exits = 'Exits: '
                for i in cordlinks:
                        self.exits += i+', '
                self.exits = self.exits[:-2]
                if 'end' in kwargs:
                        self.end = True
                else:
                        self.end = False
                if 'tele' in kwargs:
                        self.tele = kwargs['tele']
""")
for i in range(1, n+1):
      for j in range(65, 65+n):
            tile = chr(j)+str(i)+' = Place('
            Type = raw_input("Type of {}{} [Use 'sp' for unique descriptions, later on]\n".format(chr(j), str(i)))
            tile += str(Type)
            dirs = raw_input('Where can you go from here? [Use NSEWT]\n')
            dirlinks = []
            for Dir in dirs:
                  dirlinks.append(Dir.upper())
            tile += ', '+str(dirlinks)+', '
            cordlinks = []
            for Dir in dirlinks:
                  if Dir != 'T':
                        cordlinks.append( cordtable [ Dir ](j, i) )
            tile += str(cordlinks)
            if 'T' in cordlinks:
                  tile += ", tele = '{}'".format(raw_input('Teleport cords?\n'))
            end = raw_input('Is this end? [Anything for yes, enter for no]\n')
            if end != '':
                  tile += ', end = True'
            if Type == 'sp':
                  sp = raw_input('Unique description for tile...\n')
                  tile += ', sp = \'{}\''.format(sp)
            f.write(tile+')\n')
            
