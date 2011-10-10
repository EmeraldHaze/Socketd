"""
This module wraps pipes to make stdout/err flush.
"""
from sys import stdout, stdin, stderr

class Wrap:
    def __init__(self, f):
        self.f = f

    def write(self, data):
        self.f.write(data)
        self.f.flush()

    #def ___getattr__(self, item):
    #    return getattr(self.f, item)

stdout = Wrap(stdout)
stdin = Wrap(stdin)
stderr = Wrap(stderr)