from __future__ import division
from collections import Counter
import glob, os, ntpath, json, io

class TfFilter():
    def __init__(self, filepath):
        self.filepath = filepath

    def doc_tf(self,document):
        """
        For each email count return a dictionary that contains the tfs
        :param document:
        :return:
        """
        words = []
        counter = 0
        punctuation = ['(', ')', ':', ';', ',', '/', '"', " '","' ", "."]
        for word in document.split():
            for i in punctuation:
                word = word.replace(i,"")
            words.append(word.lower())
            counter += 1
        frequency = Counter(words)
        for key, value in frequency.items():
            frequency[key] = value / counter
        frequency = sorted(frequency.iteritems(),key= lambda x: x[1],
                               reverse=True)
        return frequency


    def all_tf(self):
        """
        Search all json files in directory and save a dictionary in the
        form {doc_id : {tf dictionary}
        :return:
        """
        tf ={}
        for file in glob.glob(self.filepath):
            with open(file, 'r') as fp:
                emails = json.load(fp)
                for text in emails['emails']:
                    tf[text['id']] = self.doc_tf(text['body'])
        return tf


    def number_of_docs(self):
        """
        Count the number of documents(emails) in the collection of json files
        :return:
        """
        for file in glob.glob(self.filepath):
            counter = 0
            with open(file, 'r') as fp:
                emails = json.load(fp)
                for email in emails['emails']:
                    counter +=1
        return counter


if __name__ == '__main__':
    filter = TfFilter( './files/*.json')
    filter.all_tf()
    noEmails = filter.number_of_docs()
    print filter.all_tf()

