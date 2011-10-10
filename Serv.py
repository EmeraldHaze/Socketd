#!/usr/bin/python -i
"""
This is a server that, on a connect:
A) makes an instance of a specified program
B) logs some data
C) acts as a interface between them, logging eavrything by hostname.
"""

import json
from twisted.internet import reactor, protocol, error
from time import strftime
from socket import gethostbyaddr

prg = "/I/M1/game/Maze.py"
cwd = "/I/M1/game"
port = 7000

def log(f, msg, end = "\n"):
    f.write(strftime('[%r]') + msg + end)
    f.flush()

class PrgProto(protocol.ProcessProtocol):
    """
    Process-side protocol
    """
    def __init__(self, out, dataDict):
        self.ip = dataDict['ip']
        #Out of the arguments that were passed from the client, take IP.
        try:
            hostname = gethostbyaddr(self.ip)[0]
        except:
            hostname = "UnkownHost"
        self.name = hostname+'('+str(self.ip)+')'
        self.out = out.transport
        #This is a pipe too the user
        self.log = open('Logs/'+self.name+'', 'a')
        log(self.log, 'Log opened, IP:'+self.name)
        self.stopped = False

    def outReceived(self, data):
        """
        When you get something, log it, then send it.
        """
        log(self.log, 'Proc: '+ data, end = "")
        self.out.write(data)

    def errReceived(self, data):
        """
        Errors should be logged and outputed
        """
        log(self.log, "ERROR: ", data)
        print("{}'s process has errored: {}".format(self.name, data))

    def processEnded(self, reason):
        if not self.stopped:
            if reason.check(error.ProcessDone):
                #Is it done?
                quitmsg = 'ended cleanly (The user won)'
            else:
                quitmsg = 'ended with errors!'
                reason.printDetailedTraceback(self.log)
                self.out.write('You seem to of have broken your game, you insensitive clod!')

            log(self.log, quitmsg+'\n')
            print strftime('[%r] ')+self.name+'\'s process has '+quitmsg

class PrgShell(protocol.Protocol):
    """
    This is a protocol describing what to do when someone connects to you
    """
    def connectionMade(self):
        """
        Initilize some values and increment current_users
        """
        global current_users
        current_users += 1
        self.started = False
        self.predata = ''
        #predata is the raw data recived before the start
        self.dataDict = {}
        #dataDict is the same, json-loaded

    def connectionLost(self, reason):
        global current_users
        current_users -= 1
        try:
            #This will work only if the proc(cess) is initilized
            log(self.proc.log, 'Log Closed')
            self.proc.log.close()
            print strftime('[%r]'), self.proc.name, ' has quit. There are now', current_users, 'users.'

        except AttributeError:
            #This will happen if the proc is not initilized
            print strftime('[%r]')+' Someone has quit without sending predata! [Users:', current_users, ']'
        self.proc.stopped = True
        self.proc.transport.signalProcess('KILL')
        #This will kill the child so there aren't blocked proccess all over the place

    def dataReceived(self, data):
        if self.started:
            log(self.proc.log, 'User: '+data)
            self.proc.transport.writeToChild(0, data)
            #0 is stdin
        else:
            self.predata+=data
            if self.predata[-1] == '}':
                #If the predata is ended [it's a dict]
                self.dataDict = json.loads(self.predata)
                global reactor, current_users
                self.proc = PrgProto(self, self.dataDict)
                reactor.spawnProcess(self.proc, prg, [], path = cwd)
                #Makes a proc for this user
                add(self.proc.ip)
                print strftime('[%r] ')+self.proc.name, ' has connected. There are now', current_users, 'users.'
                self.started = True

def add(ip):
    """
    This is the sequance for keeping userstats.txt and iptable.txt accurate when adding a player
    """
    stats = open("userstats.txt").read().split()
    global ipset
    ipset.add(ip)
    unique = len(ipset)
    maxu = max(int(stats[0]), current_users)
    total = str(int(stats[1])+1)
    open('userstats.txt', 'w').write(" ".join((str(maxu), str(int(total)+1), str(unique))))
    json.dump(list(ipset), open('IPs.txt', 'w'))

ipset = set(json.load(open('IPs.txt')))
current_users = 0

factory = protocol.ServerFactory()
factory.protocol = PrgShell
reactor.listenTCP(port, factory)

print 'Runing on ', port
reactor.run()