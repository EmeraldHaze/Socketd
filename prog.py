from twisted.internet import protocol

class Prog(protocol.ProcessProtocol):#, basic.Int16StringReceiver):
    """
    Program/process-side protocol
    """
    def __init__(self, users):
        self.user = users
        self.sendto = None
        self.charsleft = 0

    def childDataReceived(self, fd, data):
        if fd == 1:
            self.dataReceived(data)
        elif fd == 2:
            self.errReceived(data)

    def dataReceived(self, data):
        """
        A whole message is sent to the user specified by the first bit
        """
        #sendto = data[:1]
        #data = data[1:]
        self.user.log.write(data)
        self.user.transport.write(data)

#   dataReceived = stringReceived

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
                self.user.transport.write('You seem to of have crashed your game, you insensitive clod!')

            self.user.log.write(quitmsg)
            self.user.running = False
            print strftime('[%r] ')+self.user.name+'\'s process has '+quitmsg


