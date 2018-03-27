import sys
import getopt
import os
import math
import operator
import re

###############################Shivang Soni ######################################################
########################Cite: https://cseweb.ucsd.edu/classes/wi17/cse258-a/reports/a055.pdf #####

class NaiveBayes:
    class TrainSplit:
        """
        Set of training and testing data
        """
        def __init__(self):
            self.train = []
            self.test = []

    class Document:
        """
        This class represents a document with a label. classifier is 'pos' or 'neg' while words is a list of strings.
        """
        def __init__(self):
            self.classifier = ''
            self.words = []

    def __init__(self):
        """
        Initialization of naive bayes
        """
        self.stopList = set(self.readFile('data/english.stop'))
        self.bestModel = False
        self.stopWordsFilter = False
        self.naiveBayesBool = False
        self.numFolds = 10
        self.positiveText = {}
        self.negativeText = {}
        self.netText = {}
        self.totalPosWords = 0.0
        self.totalNegWords = 0.0
        self.totalNetWords = 0.0
        self.totalPosReviews = 0.0
        self.totalNegReviews = 0.0
        # TODO
        # Implement a multinomial naive bayes classifier and a naive bayes classifier with boolean features. The flag
        # naiveBayesBool is used to signal to your methods that boolean naive bayes should be used instead of the usual
        # algorithm that is driven on feature counts. Remember the boolean naive bayes relies on the presence and
        # absence of features instead of feature counts.

        # When the best model flag is true, use your new features and or heuristics that are best performing on the
        # training and test set.

        # If any one of the flags filter stop words, boolean naive bayes and best model flags are high, the other two
        # should be off. If you want to include stop word removal or binarization in your best performing model, you
        # will need to write the code accordingly.

    def classify(self, words):
        """
        Classify a list of words and return a positive or negative sentiment
        """
        alpha = 1
        if self.stopWordsFilter:
            words = self.filterStopWords(words)
        if self.naiveBayesBool:
            alpha = 0.7
        if self.bestModel:
            alpha = 5.2
            words = self.not_never(words)
        totalReview = self.totalPosReviews + self.totalNegReviews
        numPOS = math.log(self.totalPosReviews/totalReview)
        numNEG = math.log(self.totalNegReviews/totalReview)
        # TODO
        # classify a list of words and return the 'pos' or 'neg' classification
        # Write code here
        if self.bestModel:
         for word in list(set(words)):
          numPOS += math.log((self.positiveText.get(word,1) + alpha)/(self.totalPosWords + alpha*len(self.netText)))
          numNEG += math.log((self.negativeText.get(word,1) + alpha)/(self.totalNegWords + alpha*len(self.netText)))
        elif self.naiveBayesBool:
         for word in list(set(words)):
          numPOS += math.log((self.positiveText.get(word,1) + alpha)/(self.totalPosWords + alpha*len(self.netText)))
          numNEG += math.log((self.negativeText.get(word,1) + alpha)/(self.totalNegWords + alpha*len(self.netText)))
        else:
         for word in words:
          numPOS += math.log((self.positiveText.get(word,1) + alpha)/(self.totalPosWords + alpha*len(self.netText)))
          numNEG += math.log((self.negativeText.get(word,1) + alpha)/(self.totalNegWords + alpha*len(self.netText)))         

        if numPOS > numNEG:
           return 'pos'
        else:
           return 'neg'

    def addDocument(self, classifier, words):
        """
        Train your model on a document with label classifier (pos or neg) and words (list of strings). You should
        store any structures for your classifier in the naive bayes class. This function will return nothing
        """
        # TODO
        # Train model on document with label classifiers and words
        # Write code here
        #print(classifier,self.naiveBayesBool)
        if classifier == 'pos' and self.stopWordsFilter:
           self.totalPosReviews += 1
           for word in words:
               self.positiveText[word] = self.positiveText.get(word,0) + 1
               self.totalPosWords += 1
               self.netText[word] = self.netText.get(word,0) + 1
        elif classifier == 'neg' and  self.stopWordsFilter:
           self.totalNegReviews += 1
           for word in words:
               self.negativeText[word] = self.negativeText.get(word,0) + 1
               self.totalNegWords += 1
               self.netText[word] = self.netText.get(word,0) + 1            
        elif classifier == 'pos' and  self.naiveBayesBool:
           self.totalPosReviews += 1
           for word in list(set(words)):
               self.positiveText[word] = self.positiveText.get(word,0) + 1
               self.totalPosWords += 1
               self.netText[word] = self.netText.get(word,0) + 1
        elif classifier == 'neg' and  self.naiveBayesBool:
           self.totalNegReviews += 1
           for word in list(set(words)):
               self.negativeText[word] = self.negativeText.get(word,0) + 1
               self.totalNegWords += 1
               self.netText[word] = self.netText.get(word,0) + 1 
        elif classifier == 'pos' and  self.bestModel:
           self.totalPosReviews += 1
           for word in list(set(words)):
               self.positiveText[word] = self.positiveText.get(word,0) + 1
               self.totalPosWords += 1
               self.netText[word] = self.netText.get(word,0) + 1
        elif classifier == 'neg' and  self.bestModel:
           self.totalNegReviews += 1
           for word in list(set(words)):
               self.negativeText[word] = self.negativeText.get(word,0) + 1
               self.totalNegWords += 1
               self.netText[word] = self.netText.get(word,0) + 1
        elif classifier == 'pos':
           self.totalPosReviews += 1
           for word in words:
               self.positiveText[word] = self.positiveText.get(word,0) + 1
               self.totalPosWords += 1
               self.netText[word] = self.netText.get(word,0) + 1
        elif classifier == 'neg':
           self.totalNegReviews += 1
           for word in words:
               self.negativeText[word] = self.negativeText.get(word,0) + 1
               self.totalNegWords += 1
               self.netText[word] = self.netText.get(word,0) + 1 
                  
        pass

    def readFile(self, fileName):
        """
        Reads a file and segments.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        str = '\n'.join(contents)
        result = str.split()
        return result

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        for fileName in posDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            doc.classifier = 'pos'
            split.train.append(doc)
        for fileName in negDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            doc.classifier = 'neg'
            split.train.append(doc)
        return split

    def train(self, split):
        for doc in split.train:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            self.addDocument(doc.classifier, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            yield split

    def not_never(self, words):
      neg_feature = re.compile("^not$|never|[a-z]n't$")   # regular expression for not, n't and never
      negation = False
      neg_words = []
      for word in words:
         if (word not in (',', '.', '?', '!', ';')) & negation:
             word = "NOT_" + word
         if re.search(neg_feature, word):
             negation = True
         if word in (',', '.', '?', '!', ';'):
             negation = False
         neg_words.append(word)
      return neg_words


    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for doc in split.test:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels

    def buildSplits(self, args):
        """
        Construct the training/test split
        """
        splits = []
        trainDir = args[0]
        if len(args) == 1:
            print '[INFO]\tOn %d-fold of CV with \t%s' % (self.numFolds, trainDir)

            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    doc.classifier = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                for fileName in negDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    doc.classifier = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                split.train.append(doc)

            posDocTest = os.listdir('%s/pos/' % testDir)
            negDocTest = os.listdir('%s/neg/' % testDir)
            for fileName in posDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (testDir, fileName))
                doc.classifier = 'pos'
                split.test.append(doc)
            for fileName in negDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (testDir, fileName))
                doc.classifier = 'neg'
                split.test.append(doc)
            splits.append(split)
        return splits

    def filterStopWords(self, words):
        """
        Stop word filter
        """
        removed = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                removed.append(word)
        return removed


def test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel):
    nb = NaiveBayes()
    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    #stopWordsFilter = True
    for split in splits:
        classifier = NaiveBayes()
        classifier.stopWordsFilter = stopWordsFilter
        classifier.naiveBayesBool = naiveBayesBool
        classifier.bestModel = bestModel
        accuracy = 0.0
        for doc in split.train:
            words = doc.words
            classifier.addDocument(doc.classifier, words)

        for doc in split.test:
            words = doc.words
            guess = classifier.classify(words)
            if doc.classifier == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def classifyFile(stopWordsFilter, naiveBayesBool, bestModel, trainDir, testFilePath):
    classifier = NaiveBayes()
    classifier.stopWordsFilter = stopWordsFilter
    classifier.naiveBayesBool = naiveBayesBool
    classifier.bestModel = bestModel
    trainSplit = classifier.trainSplit(trainDir)
    classifier.train(trainSplit)
    testFile = classifier.readFile(testFilePath)
    print classifier.classify(testFile)


def main():
    stopWordsFilter = False
    naiveBayesBool = False
    bestModel = False
    (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
    if ('-f', '') in options:
        stopWordsFilter = True
    elif ('-b', '') in options:
        naiveBayesBool = True
    elif ('-m', '') in options:
        bestModel = True

    if len(args) == 2 and os.path.isfile(args[1]):
        classifyFile(stopWordsFilter, naiveBayesBool, bestModel, args[0], args[1])
    else:
        test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel)


if __name__ == "__main__":
    main()
