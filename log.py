class Log:
    """
    Nifty log file-wrapping object
    """
    def __init__(self, f):
        self.f = f
        self.lnbuff = ""

    def write(self, msg):
        msg += "\n"
        for char in msg:
            if char == "\n":
                if self.lnbuff:
                    self.f.write(strftime("[%r]") + self.lnbuff + "\n")
                    self.lnbuff = ""
            else:
                self.lnbuff += char
        self.f.flush()

    def close(self):
        self.f.close()
