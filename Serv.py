#!/usr/bin/python -i
"""
This is a server that, on a connect:
A) makes an instance of a specified program
B) logs some data
C) acts as a interface between them, logging eavrything by hostname.
"""
from twisted.protocols import basic
from twisted.internet import reactor, protocol, error
from socket import gethostbyaddr
from collections import deque
from time import strftime
from sys import stdout
import json

prg ="/I/M1/tester.py"#"/home/glycan/QFTSOM/main.py"
cwd = "/home/glycan/QFTSOM/"
port = 7000
users_needed = 2
current_users = 0
class Log:
    def __init__(self, f):
        self.f = f
        self.lnbuff = deque([""])

    def write(self, msg):
        for char in msg:
            if char == "\n":
                self.lnbuff.append("")
            else:
                self.lnbuff[-1] += char
        while self.lnbuff:
            line = self.lnbuff.popleft()
            if line:
                self.f.write(strftime("[%r]")+line+"\n")
        self.f.flush()
        self.lnbuff.append("")

    def close(self):
        self.f.close()


class User(protocol.Protocol):
    """
    This is a protocol describing what to do when someone connects to you
    """
    def connectionMade(self):
        """
        Initilize some values and increment current_users
        """
        global current_users
        current_users += 1
        self.running = False
        self.predata = ''
        #predata is the raw data recived before the start
        self.data_dict = {}
        #data_dict is the same, json-loaded

    def connectionLost(self, reason):
        """
        Adjust things and kill assoscieted resources
        """
        global current_users
        if self.running:
            print strftime('[%r]'), self.name, ' has quit. There are now', current_users, 'users.'
        else:
            print strftime('[%r]')+' Someone has quit without sending predata! [Users:', current_users, ']'

        try:
            self.prog.transport.signalProcess('KILL')
        except error.ProcessExitedAlready or AttributeError or Exception:
            pass

        current_users -= 1
        self.log.write('Log Closed')
        self.log.close()
        self.running = False

    def dataReceived(self, data):
        if self.running:
            data = ' '.join(data.split())
            self.log.write("User: "+data)
            self.prog.transport.writeToChild(0, data + "\n")
            #0 is stdin
        else:
            self.predata+=data
            if self.predata[-1] == '}':
                #If the predata is ended [it's a dict]
                self.data_dict = json.loads(self.predata)
                try:
                    self.name = names[self.data_dict['ip']]
                except KeyError:
                    self.name = self.data_dict['ip']

                self.log = Log(open('Logs/'+self.name, 'a'))
                self.log.write('Log opened')

                add(self.data_dict['ip'])
                print strftime('[%r] ')+self.name, ' has connected. There are now', current_users, 'users.'
                users.append(self)
                connect_users()


class Prog(protocol.ProcessProtocol):#, basic.Int16StringReceiver):
    """
    Program/process-side protocol
    """
    def __init__(self, users):
        self.user = users
        self.sendto = None
        self.charsleft = 0

    def dataReceived(self, data):
        """
        A whole message is sent to the user specified by the first bit
        """
        print('DTRECV')
        sendto = data[:1]
        data = data[1:]
        self.user.log.write(data)
        self.user.transport.write(data)

#    dataReceived = stringReceived

    def errReceived(self, data):
        """
        Errors should be logged and outputed
        """
        self.user.log.write("ERROR: " + data)
        print("{}'s process has errored: {}".format(self.user.name, data))

    def processEnded(self, reason):
        if self.user.running:
            if reason.check(error.ProcessDone):
                #Is it done?
                quitmsg = 'ended cleanly'
            else:
                quitmsg = 'ended with errors!'
                reason.printDetailedTraceback(self.user.log)
                self.user.transport.write('You seem to of have broken your game, you insensitive clod!')

            self.user.log.write(quitmsg)
            print strftime('[%r] ')+self.user.name+'\'s process has '+quitmsg


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

def connect_users():
    #if len(users) >= users_needed:
    if users:
        user = users.pop()
        prog = Prog(user)
        user.prog = prog
        reactor.spawnProcess(prog, prg, [], path = cwd)
        user.running = True
        print user.name, 'is running'#!~

ipset = set(json.load(open('IPs.txt')))
names = json.load(open("/I/M1/names.txt"))

users = []

factory = protocol.ServerFactory()
factory.protocol = User
reactor.listenTCP(port, factory)

print 'Runing on ~~', port
reactor.run()