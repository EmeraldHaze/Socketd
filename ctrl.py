from cmd import Cmd
from log import out
from sys import stdout
from inspect import getargspec
from pprint import pprint

class Ctrl(Cmd):
    from os import linesep as delimiter
    stop__ = False
    prompt = "\r>>> "
    undoc_header = "  \nUndocumented commands:"

    ##actions
    def do_stop(self):
        """Stops the server"""
        out.write("Stopping..")
        self.server.reactor.stop()
        self.stop__ = True

    def do_users(self):
        """pprints named_users"""
        pprint(self.server.named_users)
        print ">>> ",

    def do_value(self, attr):
        pprint(getattr(self.server, attr))
        print ">>> ",

    def do_echo(self, msg):
        """Simple echo command"""
        out.write(msg)

    def do_kick(self, user):
        "Kicks a user with extreme prejustice"
        user.transport.write("\nThe boot of destiny has been planted on your arse.")
        user.transport.loseConnection()

    def do_watch(self, user):
        "Watch a user. This sends that user's interaction to the screen"
        #Adds stdout as a file to be writen to on logging
        user.log.open(stdout, "[%s] " % user.name, "\n>>> ")
        #file, prefix, suffix

    def do_unwatch(self, user):
        "Stop watching a user. See help for watch command"
        user.log.close("<stdout>")

    def do_send(self, user, *msgs):
        "Send a message to a user"
        user.send("\nAdmin sez: " + " ".join(msgs))
        out.write("Message sent.")

    def do_whois(self, user):
        "Gives a user's IP"
        out.write(user.name + ":", user.ip)

    def do_shell(self):
        ns = {attr: getattr(self.server, attr) for attr in dir(self.server)}
        code.interact("Interactive prompt launched", local=ns)


    ##parsers
    def parse_user(self, name):
        try:
            return self.server.named_users[name]
        except KeyError:
            raise ValueError("No such user")

    ##techincal
    def init(self, server):
        #Perserves Cmd.__init__, which sets up important stuff
        self.server = server
        self.server.reactor.callLater(1.0, self.heartbeat)

    def onecmd(self, line):
        cmd, rest, line = self.parseline(line)
        if not line:
            #If the line is blank, do nothing
            return

        if cmd is None:
            #If there was no command
            return self.default(rest)

        self.lastcmd = line
        if cmd == '':
            return self.default(rest)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)

            func_args = getargspec(func).args
            args = rest.split()
            firstarg = dict(enumerate(func_args)).get(1, None)
            #Gets first arg, defaults to None. Lists don't support defaults.
            if firstarg not in ("line", "arg"):
                #if it's not a command like help
                for i, func_arg in enumerate(func_args[1:]):
                    #We don't want to think about the first arg, self
                    try:
                        arg = args[i]
                        if "parse_" + func_arg in dir(self):
                            arg = getattr(self, "parse_" + func_arg)(arg)
                        args[i] = arg

                    except ValueError as e:
                        #if the checker doesn't like something
                        return out.write(e.message)

                    except IndexError:
                        return out.write("Omitted argument", func_arg)

                return func(*args)

            else:
                return func(rest)

    def postcmd(self, stop, line):
        if self.server.state is 2:
            return True
        else:
            return self.stop__

    def default(self, line):
        self.stdout.write("No such command")

    def emptyline(self):
        #prevents cmd repeat on blank line
        pass

    def heartbeat(self):
        #print "heartbeat"
        #Wierd arcana, presumably about keeping things awake
        self.server.reactor.callLater(1.0, self.heartbeat)
