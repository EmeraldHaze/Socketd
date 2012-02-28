from twisted.internet import protocol

class User(protocol.Protocol):
    """
    This is a protocol describing what to do when someone connects to you
    It handles user-side relationships
    """
    def __init__(self):
        self.mode = 0
        self.predata = ''
        #predata is the raw data recived before the start
        self.data_dict = {}
        #data_dict is the same, json-loaded
        self.name = "no-name"

    def connectionMade(self):

        self.transport.write("Connection accepted")
        global current_users
        current_users += 1
        self.running = -1


    def connectionLost(self, reason):
        """
        Adjust things and kill assoscieted resources
        """
        global current_users
        current_users -= 1
        if self.running:
            print strftime('[%r]'), self.name, ' has quit. There are now', current_users, 'users.'
        else:
            print strftime('[%r]')+' Someone has quit without sending predata! [Users:', current_users, ']'

        try:
            self.prog.transport.signalProcess('KILL')
        except error.ProcessExitedAlready or AttributeError or Exception:
            pass

        self.log.write('Log Closed')
        self.log.close()
        self.running = False

    def dataReceived(self, data):
        #data = filter(lambda c: c.isalnum() or c.isspace() or c in '{}":', data)
        if self.running is True:
            data = ' '.join(data.split())
            self.log.write("User: "+data)
            self.prog.transport.writeToChild(0, data + "\n")
            #0 is stdin

        elif self.running is 0:
            self.name += data
            if '\n' in data:
                self.name = self.name[:-1]
                self.start()

        elif self.running is -1:
            self.predata += data
            if self.predata[-1] is '}':
                #If the predata is ended [it's a dict]
                self.data_dict = json.loads(self.predata)
                self.ip = self.data_dict["ip"]
                try:
                    self.name = names[self.data_dict['ip']]
                    self.start()
                except KeyError:
                    self.transport.write("What do you wish to be called? ")
                    self.name = ""
                    self.running = 0

    def start(self):
        """
        Sets up the log, the process, and the statistics
        """
        self.name = self.name + " (" + self.ip + ")"
        self.log = Log(open('Logs/'+self.name, 'a'))
        self.log.write('Log opened')

        add(self.data_dict['ip'])
        print strftime('[%r] ')+self.name, ' has connected. There are now', current_users, 'users.'
        users.append(self)
        connect_users()
        self.running = True
        self.prog.transport.write(str(self.name + "\n"))

