#!/usr/bin/env python
"""
This is a server that, on a connect:
A) makes an instance of a specified program
B) logs some data
C) acts as a interface between them, logging eavrything by hostname.
"""
#import readline
import json
import sys
from twisted.internet import reactor, protocol, stdio
from sys import stdout
from user import User
from ctrl import Ctrl
from log import out

STATES = ["not yet running", "running", "stopped running"]


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
    PRG = "/home/glycan/I/Socketdgames/Maze.py"
    CWD = "/home/glycan/I/Socketdgames/"
    #PRG ="/home/glycan/QFTSOM/main.py"
    #CWD = "/home/glycan/QFTSOM/"
    PORT = 7000

    def __init__(self):
        self.state = 0

        self.users = []
        self.progs = []
        self.named_users = {}
        #Users
        factory = UserFactory(self, User)
        self.reactor.listenTCP(self.PORT, factory)
        #Ctrl
        ctrl = Ctrl(stdout=out)
        ctrl.init(self)
        reactor.callInThread(ctrl.cmdloop)

        self.startup()
        self.reactor.addSystemEventTrigger("before", "shutdown", self.shutdown)

    def run(self):
        out.write("Running on", self.PORT)
        self.reactor.run()
        return None

    def startup(self):
        out.open(stdout, suffix="\n>>> ")
        out.write("Loading JSON files...")
        self.stats = json.load(open("stats.json"))
        self.IPs = json.load(open("IPs.json"))
        self.state = 1


    def shutdown(self):
        with open("stats.json", "w") as statfile:
            json.dump(self.stats, statfile, indent = 4)
            statfile.flush()

        with open("IPs.json", "w") as IPfile:
            json.dump(self.IPs, IPfile, indent = 4)
            IPfile.flush()
        out.write("\nJSON files dumped")
        self.state = 2
        out.close()

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

sys.stdout.write("\r")
sys.stdout.flush()

#prevents two >>>s on the same line. This makes the -i interactive prompt
#overwrite out prompt
