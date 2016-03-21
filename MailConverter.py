#!/usr/bin/python

from __future__ import division

import cmd
import sys


class MailConverter(cmd.Cmd):
    """Simple command processor example."""

    def __init__(self, path):
        cmd.Cmd.__init__(self)
        self.path = path

    def do_exit(self, strarg=None):
        """
        Terminate program.
        :param strarg: Python cmd specific field
        """
        sys.exit(0)

    def do_info(self, strarg=None):
        """
        Prints info about mail converter.
        :param strarg: Python cmd specific field
        """
        print("Loads text mails from given directory and exports enhanced information into json file")

    def postloop(self):
        print

if __name__ == '__main__':
    MailConverter(sys.argv[1]).cmdloop()