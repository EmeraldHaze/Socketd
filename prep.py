##This modules sole life's purupus is to make sure the IO works, the o by flushing, i by using the read() meathod with a imporvised EOL charecter intead of the standard raw_inpup, which works by read_lines()

from sys import stdout, stdin, stderr

def p(s, n = True):
    """This function replaces the print statment"""
    if n:
        s+='\n'
    #So that people can choose to strip the trailing line.
    stdout.write(s)
    stdout.flush()
    #This just so that it clears the buffer, nothing more.

def raw_input(q = '', n = False):
    """This is a workaround for client control and maing sure eavrybody gets eavrything. It acts in exactly the same why as the original."""
    p(q, n)
    #Print the query with the corect newline setting. This isn't in raw_input, but has always annoyed me.
    p('input',  False)
    #When a message ends with 'input', the client will start accepting input. Otherwise, you can't type in the server. 
    rstr = ''
    #return'd string
    cont = True
    while cont:
        #Read a charecter from the input stream, if it's \r stop, if not, add to the rstr. Rinse, lather, repeat.
        s = stdin.read(1)
        if s == '\r':
            cont = False
        else:
            rstr+=s
    return rstr
    
def input(q = '', n = False):
    return int(rawinput(q, n))
    #So thast they have a working input(), too. All of this is so that you can take any program and plug it in, so the preper has to ensure that /all/ IO works.
