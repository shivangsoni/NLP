import math, collections

class CustomModel:


  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram_count = collections.defaultdict(lambda: 0)
    self.bigram_count = collections.defaultdict(lambda: 0)
    self.trigram_count = collections.defaultdict(lambda: 0)
    self.quadgram_count = collections.defaultdict(lambda: 0)
    self.uni_words = 0
    self.vocab = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      prev_word1 = None
      prev_word2 = None
      prev_word3 = None
      for datum in sentence.data:
        word = datum.word
        self.unigram_count[tuple([word])] += 1
        if prev_word1 != None:
          self.bigram_count[tuple([prev_word1,word])] += 1
        if prev_word2 != None:
          self.trigram_count[tuple([prev_word2,prev_word1,word])] += 1
        if prev_word3 != None:
          self.quadgram_count[tuple([prev_word3,prev_word2,prev_word1,word])] += 1
        prev_word3 = prev_word2
        prev_word2 = prev_word1
        prev_word1 = word
        
    self.uni_words=sum(self.unigram_count.values())
    self.vocab=len(self.unigram_count)
     
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prev_word1 = None
    prev_word2 = None
    prev_word3 = None
    for word in sentence:
      quad_words_count = self.quadgram_count[tuple([prev_word3, prev_word2, prev_word1, word])]
      three_words_count = self.trigram_count[tuple([prev_word2, prev_word1, word])]
      two_words_count = self.bigram_count[tuple([prev_word2, prev_word1])]
      if (quad_words_count > 0):
        score += math.log(quad_words_count)
        score -= math.log(three_words_count)
      else:
        if (three_words_count > 0):
          score += math.log(1.8)
          score += math.log(three_words_count)
          score -= math.log(two_words_count)
        else:
          two_words_count = self.bigram_count[tuple([prev_word1, word])]
          one_word_count = self.unigram_count[tuple([prev_word1])]
          if (two_words_count > 0):
            score += 2*math.log(1.8)
            score += math.log(two_words_count)
            score -= math.log(one_word_count)
          else:
             score += 3 * math.log(1.8)
             score += math.log(self.unigram_count[tuple([word])] + 1.0)
             score -= math.log(self.uni_words + self.vocab)
      prev_word3 = prev_word2
      prev_word2 = prev_word1
      prev_word1 = word
    return score
