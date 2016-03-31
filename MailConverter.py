#!/usr/bin/python

from __future__ import division
from bs4 import BeautifulSoup
import cmd
import json
import os
import re
import sys


class MailConverter(cmd.Cmd):
    """Simple command processor example."""

    def __init__(self, path, category):
        cmd.Cmd.__init__(self)
        self.path = path
        self.category = category

    def do_iterate_path(self, strarg=None):
        counter = 0
        for filename in os.listdir(self.path):
            try:
                counter += 1
                x = BasicMailInformation(self.path + filename, counter, self.category)
                x.detailed_parsing(x.crude_parsing())
                with open(self.path + '/results/result.json', 'a') as fp:
                    json.dump(x.__dict__, fp)
            except IOError as e:
                pass

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


class BasicMailInformation:
    """A Basic email information as acquired by simple parsing"""

    def __init__(self, filename, counter, category):
        self.origin_file = filename
        self.counter = counter
        self.category = category
        self.senders = []
        self.content = ""
        self.subject = ""
        self.has_attachments = False
        self.has_history = False

    def print_info(self):
        print self.__dict__

    def crude_parsing(self):
        crude_list = []
        standard_fields = ["from:", "to:", "cc:", "bcc:", "mime-version:", "content-type:", "x-from:", "x-to:", "x-cc:",
                           "content-transfer-encoding:", "x-bcc:", "x-filename", "subject:", "message-id:", "x-origin:"]
        with open(self.origin_file) as f:
            for line in f:
                try:
                    line = BeautifulSoup(line, "html.parser").getText()
                except Exception as e:
                    line = ""
                line = line.lower()
                if line in ['\n', '\r\n']:
                    crude_list.append("content: " + line.strip())
                else:
                    content = False
                    for field in standard_fields:
                        if line.startswith(field):
                            content = True
                            crude_list.append(line.strip())
                    if not content and len(crude_list)>0:
                        crude_list[len(crude_list)-1] += " " + line.strip()
        return crude_list

    def detailed_parsing(self, crude_list):
        for line in crude_list:
            if line.startswith("content:"):
                self.content += line.split("content:")[1]
            if re.match("from:\s+\S+@\S+.\S+", line):
                self.senders.append(line.split("from:")[1])
            if line.startswith("x-filename"):
                self.has_attachments = len(line.split("x-filename")) > 1
            if line.startswith("subject:"):
                self.subject = line.split("subject:")[1].strip()
        self.has_history = len(self.senders) > 1

if __name__ == '__main__':
    MailConverter(sys.argv[1], sys.argv[2]).cmdloop()