from time import strftime
from sys import stdout

class Log:
    """
    Nifty log file-wrapping object
    f: the file-like object to wrap
    """
    def __init__(self, f):
        self.files = [f]
        self.lnbuff = ""

    def write(self, *msgs):
        sep = " "
        end = "\n"
        #Because you can't put complexer args in python2
        msg = sep.join(map(str, msgs)) + end
        for char in msg:
            if char == "\n":
                if self.lnbuff:
                    for f in self.files:
                        f.write(strftime("[%r] ") + self.lnbuff + "\n")
                    self.lnbuff = ""
            else:
                self.lnbuff += char
        for f in self.files:
            f.flush()

    def close(self):
        self.write("Log closed.")
        for f in self.files:
            f.close()

out = Log(stdout)
