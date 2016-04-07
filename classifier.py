import json
from collections import Counter


def getwords(document):
        """
        For each email count return a dictionary that contains the tfs
        :param document: takes as input a document (email for this one)
        :return: returns word count
        """
        words = []
        counter = 0
        punctuation = ['(', ')', ':', ';', ',', '/', '"', " '", "' ", "."]
        for word in document.split():
            for i in punctuation:
                word = word.replace(i, "")
            words.append(word.lower())
            counter += 1
        frequency = Counter(words)
        return frequency


class classifier:

    def __init__(self, getfeatures):
        # Counts of feature/category combinations
        self.fc = {}
        # Counts of documents in each category
        self.cc = {}
        self.getfeatures = getfeatures

    @staticmethod
    def getwords(self, document):
        """
        For each email count return a dictionary that contains the tfs
        :param document: takes as input a document (email for this one)
        :return: returns word count
        """
        words = []
        counter = 0
        punctuation = ['(', ')', ':', ';', ',', '/', '"', " '", "' ", "."]
        for word in document.split():
            for i in punctuation:
                word = word.replace(i, "")
            words.append(word.lower())
            counter += 1
        frequency = Counter(words)
        return frequency

    # Increase the count of a feature/category pair
    def incf(self, feature, cat):
        self.fc.setdefault(feature, {})
        self.fc[feature].setdefault(cat, 0)
        self.fc[feature][cat] += 1

    # Increase the count of a category
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    # The number of times a feature has appeared in a category
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values())

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    # Increase the count of a category
    def train(self, item, cat):
        features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for feature, fr in features.items():
            self.incf(feature, cat)

        # Increment the count for this category
        self.incc(cat)

    def prob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        #return the conditional probability of a word with a pseudoccurence
        return self.fcount(f, cat)/self.catcount(cat)

    def weighted_prob(self, f, cat, weight=1.0, as_prob=0.5):
        # Calculate current probability
        basicprob = self.prob(f, cat)
        # Count the number of times this feature has appeared in
        # all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])
        # Calculate the weighted average
        bp = ((weight*as_prob)+(totals*basicprob))/(weight+totals)
        return bp

class naivebayes(classifier):
    def docprob(self, item, cat):
        """
        use conditional probs to calculate  P(Document | 'spam/ham')
        :param item:
        :param cat:
        :return:
        """
        features = self.getfeatures(item)
        # Multiply the probabilities of all the features together
        p = 1
        for f in features:
            p *= self.weighted_prob(f, cat)
        return p

    def bayes_prob(self, item, cat):
        """
        use bayes rule to calculate the probabilities that we want in order
        to classify the document: p(Document | 'spam/ham')
        :param item:
        :param cat:
        :return:
        """
        return self.docprob(item, cat)*self.catcount(cat)/self.totalcount()

if __name__ == '__main__':
    ham_path = '../emails/ham/results/result.json'
    spam_path = '../emails/spam/results/result.json'
    cl = naivebayes(getwords)
    with open(ham_path, 'r') as fp:
                hams = json.load(fp)
                for mail in hams['ham']:
                    cl.train(mail['content'], 'ham')

    with open(spam_path, 'r') as fp:
                spams = json.load(fp)
                for mail in spams['spam']:
                    cl.train(mail['content'], 'spam')
    print cl.bayes_prob('black', 'spam'),
    with open(spam_path, 'r') as fp:
                spams = json.load(fp)
                for mail in spams['spam']:
                    cl.train(mail['content'], 'spam')
    print cl.bayes_prob('black', 'spam')

    print "is it ham? ", cl.bayes_prob('casino', 'ham'), "is it spam? ", \
        cl.bayes_prob('casino', 'spam')
