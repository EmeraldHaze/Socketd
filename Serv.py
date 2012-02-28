#!/usr/bin/python -i
"""
This is a server that, on a connect:
A) makes an instance of a specified program
B) logs some data
C) acts as a interface between them, logging eavrything by hostname.
"""

from twisted.internet import reactor, protocol, stdio
from time import strftime
from sys import stdout
import json


PRG ="/home/glycan/QFTSOM/main.py"
CWD = "/home/glycan/QFTSOM/"
PORT = 7000

class UserFactory(protocol.ServerFactory):
    def __init__(self, protocol):
        self.protocol = protocol

    def buildUser(self, addr):
        p = self.protocol()
        p.server = self.server
        self.server.users.append(p)
        return p

class Server:
    from twisted.internet import reactor
    from ctrl import Ctrl
    from user import User
    __init__(self):
        self.startup()
        self.users = []
        self.progs = []
        #Users
        factory = UserFactory(User)
        self.reactor.listenTCP(PORT, factory)
        #Ctrl
        stdio.StandardIO(Ctrl())
        #Shutdown
        self.reactor.addSystemEventTrigger("before", "shutdown", self.shutdown)

    def run():
        print "Running on", PORT
        self.reactor.run()

    def startup(self):
        self.stats = json.load(open("stats.json"))
        self.IP = json.load(open("IP.json")

    def shutdown(self):
        json.dumps(self.stats, open("stats.json", "w"), indent = 4)
        json.dumps(self.IP, open("IP.json", "w"), indent = 4)

    def add(self, IP, name):
        """
        Adds an player to IPs and the corrects the userstats
        """
        self.IPs[IP] = name
        users = len(self.users)
        if users > self.stats["max"]:
            self.stats["max"] = users
        self.stats["total"] += 1
        self.stats["unique"] = len(self.IP)

server = Server()
#reactor.spawnProcess(prog, prg, [], path = cwd)
server.run()
