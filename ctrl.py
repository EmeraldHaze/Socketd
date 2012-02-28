from twisted.protocol import basic

class Ctrl(basic.LineReceiver):
    from os import linesep as delimiter

    def lineReceived(self, line):
        print("Line recieved!")
