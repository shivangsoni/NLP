import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:  
    #         word = datum.word
    previous = "<s>"
    for sentence in corpus.corpus:
       for datum in sentence.data:
          token = datum.word
          self.unigramCounts[token] += 1
          bigram = (previous,token)   #tuple of previous and current token
          self.bigramCounts[bigram] += 1
          self.total += 1
          previous = token

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    previous = "<s>"
    for token in sentence:
      bigram = (previous,token)
      count = self.bigramCounts[bigram]
      if count > 0:
        score += math.log(count)
        score -= math.log(self.unigramCounts[previous])
      else:
        count = self.unigramCounts[token]
        score +=math.log(count + 1)
        score -=math.log(self.total + len(self.unigramCounts))
        score +=math.log(1.8)
      previous = token
      #Ignore unseen words
    return score
