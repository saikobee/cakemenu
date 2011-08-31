import sys
import os
import re

class Conf(object):
    COMMENT_RE = r'^\s+#'
    BLANK_RE   = r'^\s*$'
    DEFN_RE    = r'^\s*(\w+)\s*=\s*(.*)\s*$'

    def __init__(self):
        self.bg_sel = "#333333"
        self.fg_sel = "#33ccff"

        self.bg_norm = "#000000"
        self.fg_norm = "#cccccc"

        self.font = "Mono Bold 14"

        filename = os.path.expanduser("~/.cakemenu.conf")
        try:
            self.read_config(filename)
        except IOError:
            sys.stderr.write(
                "Could not read {filename}\n".format(filename=filename)
            )

    def read_config(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                if   self.is_comment(line): pass
                elif self.is_blank(line):   pass
                elif self.is_defn(line):    self.read_defn(line)
                else:
                    sys.stderr.write(
                        "Error reading {filename} at line {number}\n".
                            format(filename=filename, number=file.lineno)
                    )

    def is_comment(self, line): return re.match(self.COMMENT_RE, line)
    def is_blank(self,   line): return re.match(self.BLANK_RE,   line)
    def is_defn(self,    line): return re.match(self.DEFN_RE,    line)

    def read_defn(self, line):
        match = re.match(self.DEFN_RE, line)
        key = match.group(1)
        val = match.group(2)
        setattr(self, key, val)

conf = Conf()
