from __future__ import division
from collections import Counter
import glob, os, ntpath, json, io, math

class TfFilter():
    def __init__(self, filepath):
        self.filepath = filepath

    def doc_tf(self,document):
        """
        For each email count return a dictionary that contains the tfs
        :param document: takes as input a document (email for this one)
        :return: dictionary with tf scores for the document
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
            frequency[key] = value / counter + 1
        return frequency


    def global_tf(self):
        """
        Search all json files in directory and save a dictionary in the
        form {doc_id : {tf dictionary}}
        :return: dictionary in the form {doc_id : {tf dictionary}}
        """
        tf ={}
        for file in glob.glob(self.filepath):
            with open(file, 'r') as fp:
                emails = json.load(fp)
                for text in emails['emails']:
                    tf[int(text['id'])] = self.doc_tf(text['body'])
        return tf


    def number_of_docs(self):
        """
        Count the number of documents(emails) in the collection of json files
        :return: number of documents
        """
        for file in glob.glob(self.filepath):
            counter = 0
            with open(file, 'r') as fp:
                emails = json.load(fp)
                for email in emails['emails']:
                    counter +=1
        return counter

    def global_idf(self, collection, number):
        """
        Calculates idf value for each term in a Vocabulary(vocabulary is
        produced by the terms that exist in the collection of documents).
        idf is populated as follows:
        idf(t) = 1 + log( #ofdocs/ #ofdocsWithTerm + 1)
        :param collection: a dictionary containing the documents and tf scores
        :return: dictionary with term : idf_value
        """
        idf ={}
        for key, tf_dict in collection.items():
            for term in tf_dict:
                try:
                    idf[term] = idf[term] + 1
                except KeyError:
                    idf[term] = 1
        for key, value in idf.items():
            idf[key] = 1 + math.log((number / value + 1), 2)
        return idf


    def tf_Idf_global(self, global_tf, global_idf):
        """
        Calculate the tf*idf score for EACH term of EACH document
        :param global_tf: dictionary with {document : {term : tf_score}
        :param global_idf: global idf values for all documents
        :return:
        """
        tf_idf = {}
        for key,tf_dict in global_tf.items():
            tf_idf[key]={}
            for term,value in tf_dict.items():
                tf_idf[key][term] = value * global_idf[term]
        return tf_idf





if __name__ == '__main__':
    filter = TfFilter( './files/*.json')
    noEmails = filter.number_of_docs()
    global_tf = filter.global_tf()
    idf = filter.global_idf(global_tf, noEmails)
    tf_idf_dict = filter.tf_Idf_global(global_tf, idf)