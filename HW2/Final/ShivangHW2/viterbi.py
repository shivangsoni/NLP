import sys,re,collections
from collections import defaultdict, deque

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
LOG_PROB_OF_ZERO = -1000000
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5

def subcategorize(word):
    if not re.search(r'\w', word):
        return '_PUNCS_'
    elif re.search(r'[A-Z]', word):
        return '_CAPITAL_'
    elif re.search(r'\d', word):
        return '_NUM_'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)',word):
        return '_NOUNLIKE_'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', word):
        return '_VERBLIKE_'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)',word):
        return '_ADJLIKE_'
    else:
        return RARE_SYMBOL

def viterbi(brown_data,taglist,knownwords,q_values,e_values):
       prevprevtag = '*'
       prevtag = '*'
       tagged = []
       pi = defaultdict(float)
       bp = defaultdict(lambda:"PRP$")
  #print(bp)
       pi[(0, START_SYMBOL, START_SYMBOL)] = 0
       
       def S(k):
         if k in (-1, 0):
           return {START_SYMBOL}
         else:
           return taglist
       for lines in brown_data.splitlines():
            words=lines
            words=words.split() 
            n = len(words)
            wer=""
            for k in range(1, n+1):
              for u in S(k-1):
                for v in S(k):
                    max_score = 100*LOG_PROB_OF_ZERO
                    max_tag = None
                    
                    if e_values.get((v,words[k-1]), 0) != 0:
                        for w in S(k - 2):   
                            #print(e_values.get((v,words[k-1]),0))
                            score = pi.get((k-1, w, u), LOG_PROB_OF_ZERO) + \
                                    q_values.get((w, u, v), LOG_PROB_OF_ZERO) + \
                                    e_values.get((v,words[k-1]))
                            #print(w,score)
                            if score > max_score:
                                max_score = score
                                max_tag = w
                        pi[(k, u, v)] = max_score
                        bp[(k, u, v)] = max_tag
                        #print("This is max score",max_score,"This is backpointer",bp[(k, u, v)])
                        wer=wer+" "+max_tag
       #print(wer)
       max_score = 100*LOG_PROB_OF_ZERO
       u_max, v_max = None, None
       for u in S(n-1):
            for v in S(n):
                score = pi.get((n, u, v), LOG_PROB_OF_ZERO) + \
                        q_values.get((u, v, STOP_SYMBOL), LOG_PROB_OF_ZERO)
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
   trans = collections.defaultdict(lambda: 0)
   transprob = []
   for o in Trans:
     b =re.split("\s+", o.rstrip())
     t = (b[1],b[2],b[3])
     initialstates.append(b[1])
     trans[t] = float(b[4])
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

   #print(emmision)
   #print("Vocublary is\n")
   #for i in vocab:
      #print (i)
   #print(trans)
   taggedarray = viterbi(w,states,vocab,trans,emit)
   print(taggedarray)
   #print(trans.get(('PRP$', 'VBG', 'RP')))
   #print(emit.get(('UH','man')))
