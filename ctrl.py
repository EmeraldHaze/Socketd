from cmd import Cmd
from log import out
from sys import stdout
from pprint import pprint

class Ctrl(Cmd):
    from os import linesep as delimiter
    stop__ = False
    prompt = ""
    undoc_header = "  \nUndocumented commands:"

    def init(self, server):
        #Perservers Cmd.__init__, which sets up important stuff
        self.server = server
        self.server.reactor.callLater(1.0, self.heartbeat)

    def postcmd(self, stop, line):
        if self.server.state is 2:
            return True
        else:
            return self.stop__

    def do_stop(self, line):
        """Stops the server"""
        out.write("Stopping..")
        self.server.reactor.stop()
        self.stop__ = True

    def do_users(self, line):
        """pprints named_users"""
        pprint(self.server.named_users)
        print ">>> ",

    def do_echo(self, line):
        """Simple echo command"""
        out.write(line)

    def do_kick(self, line):
        "Kicks a user with extreme prejustice"
        name = line.split()[0]
        try:
            user = self.server.named_users[name]
            user.transport.write("\nThe boot of destiny has been planted on your arse.")
            user.transport.loseConnection()
        except KeyError:
            out.write("No such user")

    def do_watch(self, line):
        "Watch a user. This sends a copy of that user's interaction to the screen"
        name = line.split()[0]
        if name in self.server.named_users:
            self.server.named_users[name].log.open(
                stdout,
                "[%s] " % name,
                "\n>>> "
            )
            #Adds stdout as a file to be writen to on logging
        else:
            out.write("No such user")

    def do_unwatch(self, line):
        "Stop watching a user. See help for watch command"
        name = line.split()[0]
        if name in self.server.named_users:
            self.server.named_users[name].log.close("<stdout>")
        else:
            out.write("No such user")

    def do_send(self, line):
        "Send a message to a user"
        name, msg = line.split(" ", 1)
        try:
            self.server.named_users[name].transport.write("Admin: " + msg)
            out.write("Message sent.")
        except KeyError:
            out.write("No such user")

    def do_whois(self, line):
        "Gives a user's IP"
        name = line.split()[0]
        try:
            out.write(name + ":", self.server.named_users[name].data_dict["ip"])
        except KeyError:
            out.write("No such user,", name)

    def do_C(self, line):
        "Doesn't do anything. Serves as a comment"

    def emptyline(self):
        #prevents cmd repeat on blank line
        pass

    def heartbeat(self):
        #print "heartbeat"
        #Wierd arcana, presumably about keeping things awake
        self.server.reactor.callLater(1.0, self.heartbeat)


