from twisted.protocols import basic
from log import Log, out
from prog import Prog
import json

class User(basic.Int16StringReceiver):
    """
    This protocol handles user-side stuffs
    """
    def connectionMade(self):
        """
        Called when a user is made. This initilizes some stuff basic stuff,
        but the rest is done after ID.
        """

        self.state = 0
        self.name = None
        self.data_dict = None
        #data_dict is the json.loads'd information sent to us by the client

    def stringReceived(self, string):
        if self.state is 0 and not self.data_dict:
            #If are not running and have no data
            self.data_dict = json.loads(string)
            self.ip = self.data_dict["ip"]
            try:
                self.name = self.server.IPs[self.ip]
                self.start_prog()
            except KeyError:
                #if this IP has no registered name
                self.transport.write("What do you wish to be called? ")

        elif self.state is 0 and self.data_dict:
            #if we are not running and have data
            name = self.sanitize(string)
            if not name == string:
                #If it was changed
                name = "Cracker"
            self.name = name
            self.start_prog()

        elif self.state is 1 and self.prog.state is 1:
            #If running
            line = ' '.join(self.sanitize(string).split())
            #normalize spacing and remove bad charecters (e.g,
            #"../Server.py" as a name)
            self.log.write("User:", line)
            #0 is stdin
            self.prog.transport.writeToChild(0, line + "\n")

    def start_prog(self):
        self.name = str(self.name)
        #to prevent unicode names

        self.log = Log()
        self.log.open(self.name)

        self.server.add(self.data_dict['ip'], self.name)
        self.server.named_users[self.name] = self

        prog = Prog(self)
        self.server.reactor.spawnProcess(prog,
                self.server.PRG,
                [],
                path = self.server.CWD
            )
        self.server.progs.append(prog)
        self.prog = prog

        out.write(self.name, "had connected. Users:", len(self.server.users))
        self.transport.write("Hello, " + self.name)
        self.state = 1

    def connectionLost(self, reason):
        """
        Called when a user quits. If we are running, shuts down everything
        that we opened.
        """
        self.state = 2
        #dead

        self.server.users.remove(self)
        users = len(self.server.users)

        if self.state > 0:
            try:
                del self.server.named_users[self.name]
            except KeyError:
                out.write(self.name, "connected twice, or somehow removed his "
                    "name from the system..")

            out.write(self.name, 'has quit. Users:', users)
            self.log.close()

            if self.prog.state is not 2:
                #if it's not dead already
                self.prog.transport.signalProcess('KILL')
                self.prog.state = 2

        else:
            #if we've not started yet
            out.write("Someone without ID quit. Users:", users)

    def sanitize(self, s):
        """
        Returns s with any offending charecters removed. Specificly,
        non-(alnum|space|{}:"')
        """
        def healthy(char):
            if char.isalnum() or char.isspace() or char in '{}:"\'':
                return True
            else:
                return False

        return filter(healthy, s)

