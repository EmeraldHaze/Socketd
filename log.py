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
        self.fixes = {}
        #suffixes and prefixes
        self.lnbuff = ""

    def open(self, name, prefix="", suffix=""):
        if type(name) is str:
            f = open("Logs/" + name, "a")
        else:
            f = name
            name = f.name
        self.fixes[f] = (prefix, suffix)
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
                        prefix, suffix = self.fixes[f]
                        f.write("\r" + strftime("[%r] ") + prefix + self.lnbuff + suffix)
                    self.lnbuff = ""
            else:
                self.lnbuff += char
        for f in self.files.values():
            f.flush()

    def close(self, names=None):
        if not names:
            names = self.files.keys()
        else:
            names = [names]
        for name in names:
            try:
                self.write("Log closed.", f=name)
                f = self.files.pop(name)
                if f.name != "<stdout>":
                    f.close()
            except KeyError:
                out.write("[closing file] No file with name, %s exists" % name )

out = Log()
