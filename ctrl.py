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
        try:
            getattr(self, cmd)(args)
        except AttributeError:
            out.write("No such command")

    def watch(self, args):
        pass

    def whois(self, args):
        name = args[0]
        out.write(name + ":", self.server[name])
