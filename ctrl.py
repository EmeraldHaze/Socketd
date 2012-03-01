from twisted.protocols import basic
from log import out

class Ctrl(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, server):
        self.server = server

    def lineReceived(self, line):
        half_parsed = line.split()
        cmd = half_parsed[0]
        args = half_parsed[1:]
        if cmd in dir(self):
            getattr(self, cmd)(args)
        else:
            out.write("No such command")

    def watch(self, args):
        pass

    def whois(self, args):
        print("whois invokes")
        search_name = args[0]
        for ip, name in self.server.IPs.items():
            if name is search_name:
                out.write(name + ":", name)
                return
                #super-break
        out.write("No such name")
        #if we reached this, that means we considered every IP
