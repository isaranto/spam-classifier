#!/usr/bin/python

from __future__ import division
from nltk.corpus import stopwords, brown
from bs4 import BeautifulSoup

import json
import os
import re
import sys


def do_iterate_path(data_path, res_path, category):
    print("{0} mails...".format(category))

    counter = 0
    results = []
    for filename in os.listdir(data_path):
        try:
            counter += 1
            x = BasicMailInformation(data_path + filename, counter, category)
            x.detailed_parsing(x.crude_parsing())
            x.process_content()
            results.append(x)
        except IOError:
            pass
    with open(res_path + "/{0}.json".format(category), 'a') as fp:
        fp.write('{	"' + category + '":[')
        first = True
        for x in results:
            if first:
                first = False
            else:
                fp.write(",\n")
            json.dump(x.__dict__, fp)
        fp.write(']}')


def get_dictionary():
    x = {}
    for word in set(brown.words()):
        x[word.lower()] = 0
    print len(x.keys())
    return x


class BasicMailInformation:
    """A Basic email information as acquired by simple parsing"""

    special_chars = ["$", "?", "!", "_"]
    dictionary = get_dictionary()

    def __init__(self, filename, counter, category):
        self.origin_file = filename
        self.counter = counter
        self.category = category
        self.content = ""
        self.subject = ""
        self.char_length = 0
        self.contains_links = False
        self.num_of_unknown_words = 0
        self.num_of_special_chars = 0

    def print_info(self):
        print(self.__dict__)

    def crude_parsing(self):
        crude_list = []
        standard_fields = ["from:", "to:", "cc:", "bcc:", "mime-version:", "content-type:", "x-from:", "x-to:", "x-cc:",
                           "content-transfer-encoding:", "x-bcc:", "x-filename", "subject:", "message-id:", "x-origin:"]
        with open(self.origin_file) as f:
            for line in f:
                line = line.decode("utf-8", "ignore").encode("utf-8").lower()
                if line in ['\n', '\r\n']:
                    crude_list.append("content: " + line.strip())
                else:
                    content = False
                    for field in standard_fields:
                        if line.startswith(field):
                            content = True
                            crude_list.append(line.strip())
                    if not content:
                        if len(crude_list) > 0:
                            crude_list[len(crude_list)-1] += " " + line.strip()
                        else:
                            crude_list.append("content: " + line.strip())
        return crude_list

    def detailed_parsing(self, crude_list):
        for line in crude_list:
            if line.startswith("content:"):
                self.content += " " + line.split("content:")[1]
            if line.startswith("subject:"):
                self.subject = line.split("subject:")[1].strip()
        self.char_length = len(self.content)

    def process_content(self):
        if re.search("http://", self.content):
            self.contains_links = True
        for char in self.content:
            if char in BasicMailInformation.special_chars:
                self.num_of_special_chars += 1
        self.content = BeautifulSoup(self.content, "html.parser").getText()
        self.content = filter(None, re.split("[ \-\"\t\n\r\f\v';:.?/(),]", self.content))
        for word in self.content:
            try:
                BasicMailInformation.dictionary[word]
            except Exception:
                self.num_of_unknown_words += 1

        self.num_of_unknown_words /= (len(self.content) + 1)
        self.content = [item for item in self.content if item not in stopwords.words('english')]


if __name__ == '__main__':
    do_iterate_path(sys.argv[1], sys.argv[3], "ham")
    do_iterate_path(sys.argv[2], sys.argv[3], "spam")
