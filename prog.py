from twisted.internet import protocol, error
from log import out

class Prog(protocol.ProcessProtocol):
    """
    Program/process-side protocol
    """
    def __init__(self, user):
        self.user = user
        self.state = 0

    def connectionMade(self):
        self.state = 1

    def childDataReceived(self, fd, data):
        if fd == 1:
            self.dataReceived(data)
        elif fd == 2:
            self.errReceived(data)

    def dataReceived(self, data):
        if self.state is 1 and self.user.state is 1:
            self.user.log.write(data)
            self.user.send(data)

    def send(self, data):
        self.transport.write(data)

    def errReceived(self, data):
        """
        Errors should be logged and outputed
        """
        self.user.log.write("ERROR: " + data)
        out.write("{}'s process has errored: {}".format(self.user.name, data))

    def processEnded(self, reason):
        self.state = 2
        if self.user.state is 1:
            if reason.check(error.ProcessDone):
                #Is it done?
                quitmsg = 'cleanly'
            else:
                quitmsg = 'with errors!'
                reason.printDetailedTraceback(self.user.log)
                self.user.transport.write('You seem to of have crashed your '
                'game, you insensitive clod!')
            self.user.log.write("Ended", quitmsg)
            out.write(self.user.name + "'s process has ended", quitmsg)
            self.user.state = 2
