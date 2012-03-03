from time import strftime
from sys import stdout

class Log:
    """
    Nifty log file-wrapping object
    Used for user logs
    f: the file-like object to wrap
    """
    def __init__(self):
        self.files = {}
        self.lnbuff = ""

    def open(self, name):
        if type(name) is str:
            f = open("Logs/" + name, "a")
        else:
            f = name
            name = f.name

        self.files[name] = f
        self.write("Log opened", f=name)

    def write(self, *msgs, **options):
        defaults = {"sep": " ", "end": "\n", "f": None}
        options = dict(defaults, **options)

        if not options["f"]:
            options["f"] = self.files.keys()
        else:
            options["f"] = [options["f"]]

        msg = options["sep"].join(map(str, msgs)) + options["end"]

        for char in msg:
            if char == "\n":
                if self.lnbuff:
                    for f in options["f"]:
                        f = self.files[f]
                        f.write(strftime("[%r] ") + self.lnbuff + "\n")
                    self.lnbuff = ""
            else:
                self.lnbuff += char
        for f in self.files.values():
            f.flush()

    def close(self, names=None):
        if not names:
            names = self.files.values()
        else:
            names = [names]
        for name in names:
            try:
                f = self.files.pop(name)
                self.write("Log closed.", name)
                f.close()
            except KeyError:
                print("No file with name,", name, "exists")

out = Log()
