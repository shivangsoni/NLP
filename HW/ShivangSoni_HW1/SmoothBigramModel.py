import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """Takes a HolbrookCorpus corpus, does whatever training is needed."""
    lastword = "<s>"
    for sentence in corpus.corpus:
      for datum in sentence.data:  
        token = datum.word
        self.unigramCounts[token] += 1
        bigram = (lastword,token) 
        self.bigramCounts[bigram] += 1
        self.total += 1
        lastword = token
  
  def score(self, sentence):
    """Takes a list of strings, returns a score of that sentence."""
    score = 0.0 
    lastword = "<s>"
    for token in sentence:
      bigram = (lastword,token)
      count = self.bigramCounts[bigram]
      score += math.log(count + 1)
      score -= math.log(self.unigramCounts[lastword] + len(self.bigramCounts))
      lastword = token
    return score
