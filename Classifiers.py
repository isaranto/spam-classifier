#!/usr/bin/python

from numpy import array
from sklearn.naive_bayes import GaussianNB
import json


def load_data(data_path):
    with open(data_path) as data_file:
        data = json.load(data_file)

    x_train = []
    x_test = []
    y_train = []
    y_test = []

    for x in data["training"]:
        y_train.append(x[-1])
        x_train.append(x[:-1])

    for x in data["test"]:
        y_test.append(x[-1])
        x_test.append(x[:-1])

    return [array(x_train), array(y_train)], [array(x_test), array(y_test)]


def classify_naive_bayes(train_set, test_set):

    clf = GaussianNB()
    clf.fit(train_set[0], train_set[1])

    result = clf.predict(test_set[0])
    counter = 0

    print len(result)

    for r in range(0, len(result)):
        if result[r] == test_set[1][r]:
            counter += 1

    print counter


if __name__ == '__main__':
    train, test = load_data("/home/jah/Documents/results/fvs.json")
    classify_naive_bayes(train, test)
