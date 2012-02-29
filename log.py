from time import strftime
from sys import stdout

class Log:
    """
    Nifty log file-wrapping object
    f: the file-like object to wrap
    """
    def __init__(self, f):
        self.f = f
        self.lnbuff = ""

    def write(self, *msgs, sep=" ", end="\n"):
        msg = sep.join(msgs) + end
        for char in msg:
            if char == "\n":
                if self.lnbuff:
                    self.f.write(strftime("[%r]") + self.lnbuff + "\n")
                    self.lnbuff = ""
            else:
                self.lnbuff += char
        self.f.flush()

    def close(self):
        self.write("Log closed.")
        self.f.close()

out = Log(stdout)
