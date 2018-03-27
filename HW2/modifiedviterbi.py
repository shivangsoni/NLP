import sys,re,collections
from collections import defaultdict, deque

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
LOG_PROB_OF_ZERO = -1000
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

def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    # pi[(k, u, v)]: max probability of a tag sequence ending in tags u, v 
    # at position k
    # bp[(k, u, v)]: backpointers to recover the argmax of pi[(k, u, v)]
       tagged = []
       pi = defaultdict(float)
       bp = {}
       
    # Initialization
       pi[(0, START_SYMBOL, START_SYMBOL)] = 0.0
       
    # Define tagsets S(k)
       def S(k):
           if k in (-1, 0):
               return {START_SYMBOL}
           else:
               return taglist
       
    # The Viterbi algorithm
    #for sent_words_actual in brown_dev_words:
       sent_words = brown_dev_words
        #print(sent_words)
       n = len(brown_dev_words)
       for k in range(1, n+1):
            for u in S(k-1):
                for v in S(k):
                    max_score = float('-Inf')
                    max_tag = None
                    for w in S(k - 2):
                        if e_values.get((sent_words[k-1], v), 0) != 0:
                            print(e_values.get((sent_words[k-1], v),0))
                            score = pi.get((k-1, w, u), LOG_PROB_OF_ZERO) + \
                                    q_values.get((w, u, v), LOG_PROB_OF_ZERO) + \
                                    e_values.get((sent_words[k-1], v))
                            #print(e_values[v][sent_words[k-1]])
                            if score > max_score:
                                max_score = score
                                max_tag = w
                    pi[(k, u, v)] = max_score
                    bp[(k, u, v)] = max_tag
                    #print(max_score)
                    #print(bp[(k, u, v)])
       max_score = float('-Inf')
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
            tagged_sentence.append(sent_words_actual[j] + '/' + tags[j])
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

   #print(emit.get(('PRP$','in')))
   #print("Vocublary is\n")
   #for i in vocab:
      #print (i)
   #print(trans)
   #taggedarray = viterbi(wordList,states,vocab,trans,emit)
   #print(taggedarray)
   #print(trans.get(('PRP$', 'VBG', 'RP')))
   #print(emit.get(('UH','man')))


































































































taglist=states
pi_prob=[]

def main():
	#f1=open('gene.test','r') #test file                wordlist
	#f2=open('gene_test.p3.out','w')#output file
	k=0
	w='*'
	u='*'
	prev=1
	nos=0
        pos =""
	for line2 in wordList:
                qwe =""
		p=line2.split()
		for ww in p:
	          line=ww
	          #break
		  if(line2=='\n'):
			k=0
			w='*'
			u='*'
			prev=1
			print(line2)
		  else:
			for v in taglist:
                                #print(w,u,v)
		 		q=trans.get((w, u, v))
                                if q == None:
                                   q = 0
                                #print(q,"  ")
		 		e=emit.get((v,ww))
                                if e == None:
                                   e = 0
                                #print(e,"   ")
		 		cur=prev*q*e
		 		pi_prob.append(cur)
                                #print(cur)
		 		#print 'w=%s,u=%s,v=%s,x=%s,q=%f,e=%f'%(w,u,v,line,q,e)
		 	max_prob=max(pi_prob)
		 	if (max_prob!=0):
		 		index_v=pi_prob.index(max_prob)
		 		x=taglist[index_v]
		 		prev=max_prob
		 		del pi_prob[:]
		 		w=u
		 		u=taglist[index_v]
                                qwe = qwe + x + " "
		 		#print(x)
		 		nos=nos+1
		 		#print 'in line=',nos
		 	else:
		 		len1=len(line)
				i=0
				isnum=0
				while(i<len1):
					if(line[i].isdigit()):
						isnum=1
						rtag='NUMERIC'
					i=i+1
				if(isnum==1):
					rtag = 'CD'
                                elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)',line):
                                        rtag = 'NNP'
                                elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem)', line):
                                        rtag = 'VBG'
                                elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)',line):
                                        rtag = 'JJ'
				elif(line[len1-1].isupper() and line[:len1-1].islower()):
					rtag='LASTCAP'
				else:
					rtag='NNP'

		 		x=line+' '+rtag+'\n' 
                                qwe=qwe+ rtag +" "
		 		#prev=1
		 		del pi_prob[:]
		 		w=u
		 		u=rtag
		 		#print(x)
		 		nos=nos+1
		 		#print 'in line=',nos
	        print(qwe)	 	
        #print(pos)	 	 	
if __name__=='__main__':
	main()	

