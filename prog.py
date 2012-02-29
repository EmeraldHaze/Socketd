from twisted.internet import protocol, error
from log import out

class Prog(protocol.ProcessProtocol):
    """
    Program/process-side protocol
    """
    def __init__(self, user):
        self.user = user
        self.charsleft = 0

    #def childDataReceived(self, fd, data):
     #   if fd == 1:
      #      self.dataReceived(data)
       # elif fd == 2:
        #    self.errReceived(data)

    def dataReceived(self, data):
        """
        A whole message is sent to the user specified by the first bit
        """
        self.user.log.write(data)
        self.user.transport.write(data)

    def errReceived(self, data):
        """
        Errors should be logged and outputed
        """
        self.user.log.write("ERROR: " + data)
        out.write("{}'s process has errored: {}".format(self.user.name, data))

    def processEnded(self, reason):
        if self.user.mode is not "killed":
            if reason.check(error.ProcessDone):
                #Is it done?
                quitmsg = 'Ended cleanly'
            else:
                quitmsg = 'Ended with errors!'
                reason.printDetailedTraceback(self.user.log)
                self.user.transport.write('You seem to of have crashed your'
                'game, you insensitive clod!')

            self.user.log.write(quitmsg)
            out.write(self.user.name, "'s process has", quitmsg)
