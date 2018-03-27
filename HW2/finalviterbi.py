import sys,re,collections
from collections import defaultdict, deque

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
LOG_PROB_OF_ZERO = -1000
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5

def viterbi(brown_data,taglist,knownwords,transmat,emitmat):
  prevprevtag = '*'
  prevtag = '*'
  tagged = []
  pi = defaultdict(float)
  bp = {}
  #print(bp)
  pi[(0, START_SYMBOL, START_SYMBOL)] = 0
  for lines in brown_data.splitlines():
     words=lines
     words=words.split() 
     n = len(words)
     #print(words)
     for k in range(1,n+1):
       #tagged.append(i)
       #print(words[k-1])
       maxscore = float('-Inf')
       maxtag = None
       for u , v in transmat:
         maxscore = -9999999
         maxtag = None
          for w in transmat[(u,v)]:
              if(emitmat.get((v,words[k-1])) == None):
                 emitmat[(v,words[k-1])] = -999999
              if emitmat.get((v,words[k-1])) != 0:
                   score = pi.get((k-1, w, u), LOG_PROB_OF_ZERO) + \
                           transmat[(u,v)][w] + \
                           emitmat.get((v,words[k-1]))
                   #print(u,v,w,pi.get((k-1, w, u), LOG_PROB_OF_ZERO),transmat[(u,v)][w],emitmat.get((v,words[k-1])))
                   if score > maxscore :
                       maxscore = score
                       maxtag = w
          pi[(k,u,v)]= maxscore
          bp[(k,u,v)]= maxtag
          #print(maxscore)
          print(maxtag)
  max_score = float('-Inf')
  u_max, v_max = None, None
  for u in S(n-1):
     for v in S(n):
         score = pi.get((n, u, v), LOG_PROB_OF_ZERO) + \
                 transmat[(u,v)][STOP_SYMBOL]
         if score > max_score:
            max_score = score
            u_max = u
            v_max = v
  tags = deque()
  tags.append(v_max)
  tags.append(u_max)
        #print(tags)
  for i, k in enumerate(range(n-2, 0, -1)):
      tags.append(bp[(k+2, tags[i+1], tags[i])])
  tags.reverse()

  tagged_sentence = deque()
  for j in range(0, n):
      tagged_sentence.append(tags[j])
  tagged_sentence.append('\n')
  tagged.append(' '.join(tagged_sentence))

  return tagged


Trans_Emission = sys.argv[1]
with open(Trans_Emission) as tagFile:
   s = ''' '''
   for i in tagFile:
      s = s + i
   #for q in sys.stdin:
      #print("%s" % (q))

#####################################################################################
########  This is to make an array of words which has to be tagged ##################
#####################################################################################
   w = ''' '''
   for i in sys.stdin:
      w = w + i
   wordList = []
   
   wordList =re.split("\s+", w.rstrip())
   #print(wordList)
   #print(type(tagFile))
   #tagFile = str(tagFile)
   #for i in tagFile:
      #print("%s" % (i))   
######################################################################################
####### Making Trans and emit array ##################################################
######################################################################################
   Trans = re.findall("^trans .*$", s ,re.MULTILINE)
   #items2=re.findall("emit.*$",tagFile,re.MULTILINE)
   #for o in Trans:
     #print ("%s" % (o))
   #print("----------------------------------------------------------------------------------------------------------------")
   Emit = re.findall("^emit .*$", s ,re.MULTILINE)
   #for o in Emit:
     #print ("%s" % (o))   
   

   # d contains the list of transaction
   d = []
   t = ""
   initialstates = []
   trans = {}
   transprob = []
   for o in Trans:
     b =re.split("\s+", o.rstrip())
     t = (b[1],b[2])
     initialstates.append(b[1])
     trans[t]=defaultdict(int)
     trans[t][b[3]] = float(b[4])
     #print (trans)
     transprob.append(b[4])
     d.append(list(t))
  
   #for [x,y] in d:
     #print ("%s %s %s" %(x,y,trans[(x,y)]))
#############################################################################
##################### Number of states possible #############################
#############################################################################
   states = list(set(initialstates))
   #print (states)
#############################################################################
################# Vocabulary considered #####################################
#############################################################################
   emmision = []
   t1 = ""
   initialstates1 = []
   emit = collections.defaultdict(lambda: 0)
   vocab = []
   emitprob = []
   for o in Emit:
     b =re.split("\s+", o.rstrip())
     t = (b[1],b[2])
     initialstates1.append(b[1])
     emit[t] = float(b[3])
     emitprob.append(b[3])
     emmision.append(list(t))
     vocab.append(b[2])


   taggedarray=viterbi(w,states,vocab,trans,emit)
   print(taggedarray)
   #print(trans.get(('CC', 'UH', ',')))
   #print(emit.get(('UH','man')))
