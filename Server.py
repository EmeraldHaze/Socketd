#!/usr/bin/python -i
"""
This is a server that, on a connect:
A) makes an instance of a specified program
B) logs some data
C) acts as a interface between them, logging eavrything by hostname.
"""

from twisted.internet import reactor, protocol, stdio
import json
#from user import User
#from prog import Prog
#from ctrl import Ctrl
#from log  import Log

class UserFactory(protocol.ServerFactory):
    def __init__(self, server, protocol):
        self.protocol = protocol
        self.server = server

    def buildProtocol(self, addr):
        p = self.protocol()
        p.server = server
        self.server.users.append(p)
        return p

class Server:
    from twisted.internet import reactor
    PRG ="/home/glycan/QFTSOM/main.py"
    CWD = "/home/glycan/QFTSOM/"
    PORT = 7000

    def __init__(self):
        self.startup()
        self.users = []
        self.progs = []
        self.named_users = {}
        #Users
        from user import User
        factory = UserFactory(self, User)
        self.reactor.listenTCP(self.PORT, factory)
        #Ctrl
        from ctrl import Ctrl
        stdio.StandardIO(Ctrl(self))
        #Shutdown
        self.reactor.addSystemEventTrigger("before", "shutdown", self.shutdown)

    def run(self):
        print "Running on", self.PORT
        self.reactor.run()

    def startup(self):
        print "Loading JSON files..."
        self.stats = json.load(open("stats.json"))
        self.IPs = json.load(open("IPs.json"))

    def shutdown(self):
        with open("stats.json", "w") as statfile:
            json.dump(self.stats, statfile, indent = 4)
            statfile.flush()

        with open("IPs.json", "w") as IPfile:
            json.dump(self.IPs, IPfile, indent = 4)
            IPfile.flush()
        print "\nJSON files dumped"

    def add(self, IP, name):
        """
        Adds an player to IPs and the corrects the userstats
        """
        self.IPs[IP] = name
        users = len(self.users)
        if users > self.stats["max"]:
            self.stats["max"] = users
        self.stats["total"] += 1
        self.stats["unique"] = len(self.IPs)

server = Server()
server.run()
