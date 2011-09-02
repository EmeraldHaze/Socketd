"""This whole server thing is nothing but a somewhat complicated server that makes an instance of a preped program when someone conencts, and acts as a interface between them, logging eavrything by hostname."""
from twisted.internet import reactor, protocol, error
#In order: Makes the whole thing run, allows for talking to process and other people, used for checking what happened to process
from time import strftime
#Used for the time in the logs
from socket import gethostbyaddr
#We'll use this to get the name in the logs
import json
#To get the startup config details

class PrgShell(protocol.Protocol):
    """This is a protocol describing what to do when someone connects to you"""
    class PrgProto(protocol.ProcessProtocol):
        """Process-side protocol. This, and the above, is why we got twisted.internet.protocol"""
        def __init__(self, out, dataDict):
            """When a instance of PrgProto is made, do all this"""
            #out is simply the protocol that's connected to the client
            self.ip = dataDict['ip']
            #Out of the arguments that were passed from the client, take IP.
            try:
                self.name = gethostbyaddr(self.ip)[0]+'('+str(self.ip)+')'
                #And get the hostname from the IP, for use as a name, with the IP too, since we seem to be geting a lot of same-names (I think it's becouse of people not being listed in DNSes)
            except:
                    self.name = 'UnknownHost'+'('+str(self.ip)+')'
            
            self.transportout = out.transport
            #This is so we can send messages to the person who's using out instance, and make other referances to out conection.
            self.log = open('Logs/'+self.name+'', 'a')
            #This is, of course, a log file for this particular person
            self.log.write(strftime('[%r]')+'Log opened, IP:'+self.name+'\n')
            #Write to the log when (strftime('[%r]') stands for put the time current time in format r in brakets) it was opened, and by whom.
            self.log.flush()
            #Flush the buffer, ensure that the data gets there. I won't explain this or the time anymore
            

        def outReceived(self, data):
            """You get something, you log it, you send it."""
            self.log.write(strftime('[%r]')+'Proc: '+ data)
            #Write what we got (rembere, this is called when the instance of the program gets sens something to output) to the log, with the time, and a note that it's from the process
            self.log.flush()
            self.transportout.write(data)
            #..and send it to the person who should see it
            
        def processEnded(self, reason):
            if reason.check(error.ProcessDone):
                #A bit complicated... Check if the reason for ending the process is a done process (we got error so that we could reference this). Since it returns None if it's not, (which evalutates to flase in this case) and error.ProcessDone (which evalutates to true), we don't have to put any ==s our stuff
                quitmsg = 'Ended Cleanly (The user won)'
                #The quit message (see below) is what you read. The program can only end if the user won, you know
            else:
                quitmsg = 'Ended with errors!'
                reason.printDetailedTraceback(self.log)
                #Failures (what the reason is) have printTraceback meathods. I'm invoking the detailed one which will write to the log, so that I can trace the error if need be.
                self.transportout.write('You seem to of have broken your game, you insensitive clod!')
                #So that the user doesn't think his game crashed, even though it did. :p
            self.log.write(strftime('[%r]')+quitmsg+'\n')
            #Log the time and quitmessage
            self.log.flush()
            print strftime('[%r] ')+self.name+'\'s process has '+quitmsg
            #And print it for good mesure, since process endings are rare. I might want to congradulate or kill them personally, you know. (Dependaning on the previce if/else sequance)
            
    #Now, the user side of it. It's almost the same thing, except when it isn't.
    def connectionMade(self):
        """This will preper the instance to wait for some prelimeries, e.g. the ip."""
        self.started = False
        self.predata = ''
        self.dataDict = {}
        
    def connectionLost(self, reason):
        global users
        try:
            self.proto.log.write('\n'+strftime('[%r]')+'Log Closed\n')
            self.proto.log.flush()
            users-=1
            print strftime('[%r]')+self.proto.name, ' has quit. There are now', users, 'users.'
            self.proto.log.close()
        except:
            print strftime('[%r]')+' Someone has quit without sending predata!'
        #Try identifying the quiter and writeing to his log, which won't work if there was no process made (if he quit before identifying himself)
        
    def dataReceived(self, data):
        if self.started:
            data.replace('\r', '')
            #I use \r for EOL to talk to the subprocess, so I strip the message of \rs.
            data.replace('\n', '')
            #newlines could be inconvientient on the other end. See prep.py
            self.proto.log.write('\n'+strftime('[%r]')+'User: '+data+'\n')
            self.proto.log.flush()
            #Log it.
            self.proto.transport.writeToChild(0, data+'\r')
            #Send it to the child over the input chnal, and end it with the EOL
        else:
            self.predata+=data
            if self.predata[-1] == '}':
                #If the predata is finished
                self.dataDict = json.loads(self.predata)
                #Format the data as a dict for PrgProto.__init__
                global reactor, users
                #this is so that we can change users and use the rector
                self.proto = self.PrgProto(self, self.dataDict)
                #Make an instance of the protocol which we can later send stuff through, with a copy of us so that they can send stuff to us, too
                addr = "/home/glycan/Documents/Python/Maze/Maze.py"
                ###THIS IS WHAT YOU HAVE TO CHANGE TO MATCH YOUR PROGRAM.
                reactor.spawnProcess(self.proto, addr, ['Maze.py'])
                #Use the reactor to make a new process at addr, with which we will interact as per self.proto, who's argv[0] must, of course, be itself (that's the array)
                users+=1
                #If someone joins, there is one more user. Iron logic!
                more(self.proto.ip)
                #This is a sequance for updating userstats.txt, which says the max total users and total connetions.
                print strftime('[%r] ')+self.proto.name, ' has connected. There are now', users, 'users.'
                #Report when, who, and how many people there are now
                self.started = True
                #Turn normal data reciveding on.
def more(ip):
    """This is the sequance for updateing userstats.txt. It's -has-hasn't been done in one line, for greater legibilty. It hardly bears explaining. Those not faint of heart, contintiue!"""
    global users, iptable
    if ip not in iptable:
        iptable.append(ip)
    unique = len(iptable)
    maxu = max(int(open('userstats.txt').read().split()[0]), users)
    tot = int(open('userstats.txt').read().split()[1])
    open('userstats.txt', 'w').write(str(maxu) +' '+str(tot+1)+' '+str(unique))
    json.dump(iptable, open('iptable.txt', 'w'))
iptable = json.load(open('iptable.txt'))
users = 0
#The total users currently connected
port = 7000
#What port the server runs on
factory = protocol.ServerFactory()
factory.protocol = PrgShell
#Out-of-the box factory (protocol maker) where we specift'd 
reactor.listenTCP(port, factory)
#This is how and where to run
print 'Runing on ', port
reactor.run()
#...and Run! For your life, obviously, becouse if this wreck of a server caches you, you will DIE. (From the horror)
