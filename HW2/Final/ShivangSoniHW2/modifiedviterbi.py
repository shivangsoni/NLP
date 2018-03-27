import sys,re,collections
from collections import defaultdict, deque

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
LOG_PROB_OF_ZERO = -99999
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
OOV_WORD="OOV"

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
   w = ""
   for i in sys.stdin:
      w = w + i
   
   wordList =re.split("\n+", w.rstrip()) 
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


taglist=states
pi_prob=[]

def main():
	#f1=open('gene.test','r') #test file                wordlist
	#f2=open('gene_test.p3.out','w')#output file
	k=0
	w='*'
	u='*'
	prev=-1000000
	nos=0
        pos =""
	for line2 in wordList:
                #print(line2)
                qwe =""
		p=line2.split()
		for ww in p:
	          line=ww
                  #if ww not in vocab:
                     #ww=OOV_WORD
                  #print(ww)
	          #break
		  if(line2=='\n'):
			k=0
			w='*'
			u='*'
			prev=-1000000
			print(line2)
		  else:
			for v in taglist:
                                #print(w,u,v)
		 		q=trans.get((w, u, v),-1000000)
                                if q == None:
                                   q = -1000000
                                #print(q,"  ")
		 		e=emit.get((v,ww),-1000000)
                                if e == None:
                                   e = -1000000
                                #print(e,"   ")
		 		cur=prev+q+e
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
                                if qwe == "":
                                   qwe = x
                                else:
                                   qwe = qwe + " " + x
		 		#print(x)
		 		nos=nos+1

	        print(qwe) 	 	
if __name__=='__main__':
      main()	

