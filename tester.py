#!/usr/bin/python
from sys import stdout, stdin, stderr


stdout.write("Hello world\nQuery:")
stdout.flush()
a = stdin.readline()
stdout.write("You said: "+a)
stdout.flush()
f = open("logfile", 'w')
f.write("The user said: "+a)
f.close()
#~
#~ class Wrap:
    #~ def __init__(self, f):
        #~ self.f = f
    #~ def write(self, data):
        #~ self.f.write(data)
        #~ self.f.flush()
    #~ def __getattr__(self, item):
        #~ return getattr(self.f, item)
#~
#~ stdout = Wrap(stdout)
#~ stdin = Wrap(stdin)
#~ stderr = Wrap(stderr)
#~
#~ print 'a'
#~ import time
#~ f = open("FILE", 'w')
#~ print 'MOO!'
#~ while 1:
    #~ c = stdin.read(1)
    #~ f.write(c)
    #~ f.flush()
    #~ print c
    #~ stdout.write(c)
    #~ stdout.f.flush