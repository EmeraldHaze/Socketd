from twisted.internet import reactor, protocol, error

class Prog(protocol.ProcessProtocol):#, basic.Int16StringReceiver):
    """
    Program/process-side protocol
    """
    def childDataReceived(self,fd, data):
        """
        A whole message is sent to the user specified by the first bit
        """
        print('DTRECV')
        print(data)

prog = Prog()
reactor.spawnProcess(prog, "python", ["python", "tester.py"])
print("Running")
reactor.run()

##tester.py
#!/usr/bin/python
from sys import stdout, stdin, stderr


stdout.write("Hello world\nQuery:")
stdout.flush()
a = stdin.readline()
stdout.write("You said: "+a)
stdout.flush()
f = open("logfile", 'w')
f.write("The user said: "+a)
f.close()