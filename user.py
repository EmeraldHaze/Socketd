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
        self.modes = ["pre", "ID", "start", "run", "killed"]
        self.mode = "pre"
        self.name = "no-name"

        #data_dict is the json.loads'd information sent to us by the client
        self.data_dict = {}

    def connectionLost(self, reason):
        """
        Called when a user quits. If we are running, shuts down everything
        that we opened.
        """
        if self.mode is not "pre":
            self.server.users.remove(self)
            users = len(self.server.users)

        if self.mode is "run":
            del self.server.named_users[self.name]
            out.write(self.name, 'has quit. Users:', users)
            self.log.close()
            if self.mode is "run":
                self.prog.transport.signalProcess('KILL')
                self.prog.mode = "killed"
        elif self.mode is not "pre":
            #If it's not run, and it's not pre (=ID)
            out.write("Someone without ID quit. Users:", users)

        self.mode = "killed"

    def stringReceived(self, string):
        if self.mode is not "pre":
            self.sanitize(string)

        if self.mode is "pre":
            self.data_dict = json.loads(string)
            self.ip = self.data_dict["ip"]
            try:
                self.name = self.server.IPs[self.ip]
                self.mode = "start"
                self.start_prog()
            except KeyError:
                #if this IP has no name
                self.transport.write("What do you wish to be called? ")
                self.mode = "ID"

        elif self.mode is "ID":
            name, crack = self.sanitize(string)
            if crack:
                name = "Cracker"
            self.name = name
            self.mode = "start"
            self.start_prog()

        elif self.mode is "run":
            line = ' '.join(string.split())
            #normalize spacing
            self.log.write("User:", line)
            #0 is stdin
            self.prog.transport.writeToChild(0, line + "\n")

    def start_prog(self):
        self.name = str(self.name)
        #to prevent unicode names

        self.log = Log(open('Logs/'+self.name, 'a'))
        self.log.write('Log opened')

        self.server.add(self.data_dict['ip'], self.name)
        self.server.named_users[self.name] = self

        self.mode = "run"

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

    def sanitize(self, s):
        """
        Returns s with any offending charecters removed. Specificly,
        (cleans, anything-removed?)
        """
        def healthy(char):
            if char.isalnum() or char.isspace() or char in '{}:"\'':
                return True
            else:
                return False

        return (filter(healthy, s),
            not (s.isalnum() or s.isspace() or s in '{}:"\''))

