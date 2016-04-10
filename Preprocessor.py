#!/usr/bin/python

import json


class Preprocessor:
    """
    Preprocessor class: Responsible for converting mail instances into feature vectors and separating data into
    training and test data set.
    """

    def __init__(self, data_path, categories):
        self.path = data_path
        self.categories = categories
        self.features = []
        self.extra_features = []
        self.data = {"training": [], "test": []}

    def load_features(self):
        for category in self.categories:
            print category
            with open(self.path + category + "_features.json") as data_file:
                words = json.load(data_file)
                self.features.extend(words)

    def extend_features(self):
        self.extra_features = ["char_length", "contains_links", "num_of_unknown_words", "num_of_special_chars"]

    def load_data(self):
        training_data = []
        test_data = []
        for category in self.categories:
            print category
            with open(self.path + category + ".json") as data_file:
                data = json.load(data_file)[category]
                training_data.extend(data[len(data)/5:])
                test_data.extend(data[:len(data)/5])
        return training_data, test_data

    def convert_mail_to_fv(self, mail):
        fv = []
        for feature in self.extra_features:
            fv.append(mail[feature])

        for feature in self.features:
            fv.append(feature in mail["content"])

        fv.append(mail["category"])

        for i in range(0, len(fv)):
            if fv[i] == True or fv[i] == "spam":
                fv[i] = 1
            elif fv[i] == False or fv[i] == "ham":
                fv[i] = 0

        return fv


if __name__ == '__main__':
    y = Preprocessor("/home/jah/Documents/results/", ["spam", "ham"])
    y.extend_features()
    y.load_features()
    y.data["training"], y.data["test"] = y.load_data()

    for i in range(0, len(y.data["training"])):
        y.data["training"][i] = y.convert_mail_to_fv(y.data["training"][i])
    for i in range(0, len(y.data["test"])):
        y.data["test"][i] = y.convert_mail_to_fv(y.data["test"][i])

    with open("/home/jah/Documents/results/fvs.json", "w") as fvs:
        json.dump(y.data, fvs)
