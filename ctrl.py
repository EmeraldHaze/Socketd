from twisted.protocols import basic
from log import out
from sys import stdout

class Ctrl(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, server):
        self.server = server

    def lineReceived(self, line):
        half_parsed = line.split()
        cmd = half_parsed[0]
        try:
            args = half_parsed[1:]
        except IndexError:
            args = []
        if cmd in dir(self):
            getattr(self, cmd)(args)
        else:
            out.write("No such command")

    def watch(self, args):
        name = args[0]
        if name in self.server.named_users:
            self.server.named_users[name].log.open(stdout)
            #Adds stdout as a file to be writen to on logging
        else:
            out.write("No such user")

    def unwatch(self, args):
        name = args[0]
        if name in self.server.named_users:
            self.server.named_users[name].log.close("<stdout>")
            #Adds stdout as a file to be writen to on logging
        else:
            out.write("No such user")

    def whois(self, args):
        print("whois invoked")
        search_name = args[0]
        for ip, name in self.server.IPs.items():
            if name is search_name:
                out.write(name + ":", ip)
                return
                #ends the function right here
        out.write("No such name")
        #if we reached this, that means we considered every IP
