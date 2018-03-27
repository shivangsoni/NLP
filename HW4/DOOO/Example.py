import sys
import getopt
import os
import math
import re

class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('data/english.stop'))
    self.numFolds = 10

    self.posText = {}   # mega text for positve reviews, with frequency
    self.negText = {}   # mega text for negative reviews, with frequency
    self.text = {}     # mega text for all reviews
    self.numPosWords = 0.0    # total number of words in positve mega text
    self.numNegWords = 0.0    # total number of words in negatvie mega text
    self.numPosReviews = 0.0    # number of positive reviews
    self.numNegReviews = 0.0    # number of negative reviews
    
    self.NEGATION_FEATURES = True

  def classify(self, words):
    """
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    numTotalReviews = self.numPosReviews + self.numNegReviews
    probPos = math.log(self.numPosReviews / numTotalReviews)    # Prior of positive reviews
    probNeg = math.log(self.numNegReviews / numTotalReviews)    # Prior of negative reviews


    for word in words:
      probPos += math.log((self.posText.get(word,0) + 1)/(self.numPosWords + len(self.text) + 1)) # add-1 smoothing and add one for unknown words
      probNeg += math.log((self.negText.get(word,0) + 1)/(self.numNegWords + len(self.text) + 1)) 

    if probPos > probNeg:
      return 'pos'
    else:
      return 'neg'

  def addExample(self, klass, words):
    """
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier
     * in the NaiveBayes class.
     * Returns nothing
    """
    if klass == 'pos':
      self.numPosReviews += 1
      for word in words:              # use this line for regular Naive Bayes method
      # for word in list(set(words))  # use this line for Boolean Naive Bayes method
        self.posText[word] = self.posText.get(word,0) + 1
        self.numPosWords += 1
        self.text[word] = self.text.get(word,0) + 1
    else:
      self.numNegReviews += 1
      for word in words:              # use this line for regular Naive Bayes method
      # for word in list(set(words))  # use this line for Boolean Naive Bayes method
        self.negText[word] = self.negText.get(word,0) + 1
        self.numNegWords += 1
        self.text[word] = self.text.get(word,0) + 1

    pass

  def filterStopWords(self, words):
    """
    * Filters stop words found in self.stopList.
    """
    filtered_words =[]
    for word in words:
        if word not in self.stopList:
            filtered_words.append(word)
    return filtered_words
    
  def negationFeatures(self, words):
    """
    * Detect negation words (not, n't and never) and add NOT_ to each word
      until the next puctuation.
    * Use regular expressions
    """
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


  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents))
    return result


  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()


  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      if self.NEGATION_FEATURES:
        words = self.negationFeatures(words)
      self.addExample(example.klass, words)

  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = []
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits

  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels

  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = []
    testData = []
    splits = []
    trainDir = args[0]
    if len(args) == 1:
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fold in range(0, self.numFolds):
        split = self.TrainSplit()
        for fileName in posTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        splits.append(split)
    elif len(args) == 2:
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
        example.klass = 'neg'
        split.test.append(example)
      splits.append(split)
    return splits

def main():
  nb = NaiveBayes()

  # default parameters: no stop word filtering, and
  # training/testing on ../data/imdb1
  if len(sys.argv) < 2:
      options = [('','')]
      args = ['data/imdb1/']
  else:
      (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True

  splits = nb.buildSplits(args)
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words = classifier.filterStopWords(words)
      if nb.NEGATION_FEATURES:
        words = classifier.negationFeatures(words)
      classifier.addExample(example.klass, words)

    for example in split.test:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words = classifier.filterStopWords(words)
      if nb.NEGATION_FEATURES:
        words = classifier.negationFeatures(words)
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    main()
