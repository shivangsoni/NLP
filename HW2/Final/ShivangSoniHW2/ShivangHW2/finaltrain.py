
#!/usr/bin/python

# David Bamman
# 2/14/14
#
# Python port of train_hmm.pl:

# Noah A. Smith
# 2/21/08
# Code for maximum likelihood estimation of a bigram HMM from 
# column-formatted training data.

# Usage:  train_hmm.py tags text > hmm-file

# The training data should consist of one line per sequence, with
# states or symbols separated by whitespace and no trailing whitespace.
# The initial and final states should not be mentioned; they are 
# implied.  
# The output format is the HMM file format as described in viterbi.pl.

import sys,re
import math
import numpy as np
from itertools import izip
from collections import defaultdict



TAG_FILE=sys.argv[1]
TOKEN_FILE=sys.argv[2]

vocab={}
OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

emissions={}
transitions={}
transitionsTotal=defaultdict(int)
emissionsTotal=defaultdict(int)

with open(TAG_FILE) as tagFile, open(TOKEN_FILE) as tokenFile:
        count=0
	for tagString, tokenString in izip(tagFile, tokenFile):
                count = count + 1
                if(count == 40000):
                  break
		tags=re.split("\s+", tagString.rstrip())
		tokens=re.split("\s+", tokenString.rstrip())
		pairs=zip(tags, tokens)
                #count = count + 1
		prevtag=INIT_STATE
                prevprevtag=INIT_STATE
		for (tag, token) in pairs:
			# this block is a little trick to help with out-of-vocabulary (OOV)
			# words.  the first time we see *any* word token, we pretend it
			# is an OOV.  this lets our model decide the rate at which new
			# words of each POS-type should be expected (e.g., high for nouns,
			# low for determiners).

			if token not in vocab:
				vocab[token]=1
				token=OOV_WORD

			if tag not in emissions:
				emissions[tag]=defaultdict(int)
                        if prevprevtag not in transitions:
                                #transitions[prevprevtag]=defaultdict(lambda:defaultdict(int))
			    if prevtag not in transitions:
				transitions[(prevprevtag,prevtag)]=defaultdict(int)

			# increment the emission/transition observation
			emissions[tag][token]+=1
			emissionsTotal[tag]+=1
			transitions[(prevprevtag,prevtag)][tag]+=1
			transitionsTotal[(prevprevtag,prevtag)]+=1
                        prevprevtag=prevtag
			prevtag=tag

		# don't forget the stop probability for each sentence
		if prevprevtag not in transitions:
			#transitions[prevprevtag]=defaultdict(lambda:defaultdict(int))
		    if prevtag not in transitions:
			 transitions[(prevprevtag,prevtag)]=defaultdict(int)

		transitions[(prevprevtag,prevtag)][FINAL_STATE]+=1
		transitionsTotal[(prevprevtag,prevtag)]+=1


for prevprevtag,prevtag in transitions:
	#for prevtag in transitions[prevprevtag]:
            t=(prevprevtag,prevtag)
            for tag in transitions[t]:
		print "trans %s %s %s %s" % (prevprevtag, prevtag, tag,  math.log(float(transitions[t][tag]) / transitionsTotal[t]))

for tag in emissions:
	for token in emissions[tag]:
		print "emit %s %s %s" % (tag, token, math.log(float(emissions[tag][token]) / emissionsTotal[tag]))





def deleted_interpolation(unigram_c, bigram_c, trigram_c):
    lambda1 = lambda2 = lambda3 = 0
    for a, b, c in trigram_c.keys():
        v = trigram_c[(a, b, c)]
        if v > 0:
            try:
                c1 = float(v-1)/(bigram_c[(a, b)]-1)
            except ZeroDivisionError:
                c1 = 0
            try:
                c2 = float(bigram_c[(a, b)]-1)/(unigram_c[(a,)]-1)
            except ZeroDivisionError:
                c2 = 0
            try:
                c3 = float(unigram_c[(a,)]-1)/(sum(unigram_c.values())-1)
            except ZeroDivisionError:
                c3 = 0

            k = np.argmax([c1, c2, c3])
            if k == 0:
                lambda3 += v
            if k == 1:
                lambda2 += v
            if k == 2:
                lambda1 += v

    weights = [lambda1, lambda2, lambda3]
    norm_w = [float(a)/sum(weights) for a in weights]
    return norm_w
