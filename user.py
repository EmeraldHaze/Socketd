from twisted.protocols import basic
from log import Log, out
from Serv import PRG, CWD
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

        self.predata = ''
        #predata is the raw data recived before the start
        self.data_dict = {}
        #data_dict is the same, json-loaded

    def connectionLost(self, reason):
        """
        Called when a user quits. If we are running, shuts down everything
        that we opened.
        """
        self.server.users.remove(self)
        users = len(self.server.users)
        if self.mode is "run":
            out.write(self.name, 'has quit. Users:', users)
            self.log.close()
            if self.prog.mode = "run":
                self.prog.transport.signalProcess('KILL')
                self.prog.mode = "killed"
        else:
            out.write("Someone without ID quit. Users:", users))
        self.mode = "killed"

    def stringReceived(self, string):
        if self.mode is "pre":
            self.data_dict = json.loads(self.predata)
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
            self.name = string
            self.mode = "start"
            self.start_prog()

        elif self.mode is "run":
            data = ' '.join(data.split())
            #normalize spacing
            self.log.write("User: "+data)
            self.prog.transport.send(0, data + "\n")
            #0 is stdin

    def start(self):
        from prog import Prog
        self.server.reactor.spawnProcess(prog, PRG, [], path = CWD)
        self.log = Log(open('Logs/'+self.name, 'a'))
        self.log.write('Log opened')
        add(self.data_dict['ip'])
        print strftime('[%r] ')+self.name, ' has connected. There are now', current_users, 'users.'
