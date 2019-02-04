# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:16:59 2019

@author: rksazid
"""

import NameRecognition as nr
import PronounReplacement as pr
import CosineSimilarity as csim
import BanglaStemmer as bs
import BanglaTokenization as bnTok
import NumericFigure as nf
import tfidf
from copy import deepcopy
from operator import attrgetter
import math

# Sentence Class that contains every attributes of a sentence
class Sentences:
    def __init__(self, idx, ln, wrds):
        self.index = idx
        self.line = ln
        self.words = wrds
        self.tfidf = 0.00
        self.sf = 1.00
        self.score = 0.00
        self.cos_sim = []
        self.names = []
        self.subj_noun=[]
        self.obj_noun=[]
        self.tw = 0.0
        self.nc = 0.0
        self.status = True


    
#================================ MAIN ========================================

#input
path='.\Dataset1\Documents\Document_2.txt'

input_file = open(path,'r', encoding='utf-8')
doc=input_file.read()

#tokenization
bn_tokens = bnTok.BengaliTok(doc,"general")
bn_tokens.bn_stop_words()
tokenized_sentences = bn_tokens.bn_sentence_tok(r'[?|।|!]')
tokenized_words = bn_tokens.bn_word_tok(tokenized_sentences)

#make a list of Sentence class
sentences_list = []
ln = len(tokenized_words)
#print(ln)
#print(tokenized_words)
#print(tokenized_sentences)


for i in range(ln):
    #print(tokenized_sentences[i])
    if tokenized_sentences[i]:
        sentences_list.append(Sentences(i,tokenized_sentences[i],
                                        tokenized_words[i]))


#=============================== nf Consideration============================

nf.BanglanumericDetection(sentences_list)


#============================== Stemming ======================================

for obj in sentences_list:
    obj.words=bs.stemming(obj.words)

#========================== Name recognition  =================================

for obj in sentences_list:
    names = nr.nameRecognition(deepcopy(obj.words))
    obj.names += names

#===================== TF-IDF Calcualtion For every sentence ==================

# make a list of all token in a document
tokenized_documents = []
for lst in tokenized_words:
    tokenized_documents += tokenized_words[lst]


#tf-idf calculation start
tfidf_obj = tfidf.TFIDF()

i=0
for obj in sentences_list:
    tfidf=0
    for word in obj.words:
        tfidf+=tfidf_obj.tf_idf(word,tokenized_documents,
                                ' '.join(tokenized_sentences))
    sentences_list[obj.index].tfidf=tfidf


#======================== Cosine Similarity Calculaion ========================

for i in range(ln):
    for j in range(ln):
        if i != j:
            w1=sentences_list[i].words
            w2=sentences_list[j].words
            cosine_sim = csim.cosSim(w1,w2)
            sentences_list[i].cos_sim.append(cosine_sim)
        else:
            sentences_list[i].cos_sim.append(0.0)

#======== Sentence Redundancy elemeation using cosine similarity value ========
   
for i in range(1,ln):
    for j in range(1,ln):
        if i == j:
            continue
        elif sentences_list[i].cos_sim[j] > 0.6:
            if len(sentences_list[i].line) > len(sentences_list[j].line):
                sentences_list[i].sf+=1
                sentences_list[j].status = False
            else :
                sentences_list[j].sf+=1
                sentences_list[i].status = False
                
#================== Title word score calculation =============================

title_words = bn_tokens.title
for obj in sentences_list:
    for w in title_words:
        if w in obj.words:
            obj.tw+=1.0


for obj in sentences_list:
    print("")
    print(obj.index,obj.line,obj.words,obj.tfidf,obj.cos_sim,obj.status,
                                      obj.names,obj.tw,obj.nc)

#========================= Sentence Selection =================================

if sentences_list[0].tw > 0:
    sentences_list[0].score = 1000

summary = ""
summary_list=[]
w1=1
w2=1
w3=1
w4=1
for obj in sentences_list:
    if obj.index > 0:
        obj.score = w1*obj.tfidf+ w2*obj.sf + w3*obj.nc + w4*obj.tw
    else:
        if sentences_list[0].tw > 0:
            obj.score = 1000
        else:
            obj.score = w1*obj.tfidf+ w2*obj.sf + w3*obj.nc + w4*obj.tw

print("")
for obj in sentences_list:
    print(obj.index, obj.score)

sentences_list.sort(key=attrgetter('score'),reverse=True)
print("")
for obj in sentences_list:
    print(obj.index, obj.score)

for obj in sentences_list:
    if obj.status:
        summary_list.append(deepcopy(obj))
print("")
for obj in summary_list:
    print(obj.index, obj.score)

sz = math.ceil((len(sentences_list)/3))
print(sz)

final_list = []
i=0
for obj in summary_list:
    if i<sz:
        final_list.append(obj)
    i+=1
print("")
for obj in final_list:
    print(obj.index, obj.score)

final_list.sort(key=attrgetter('index'))

print("")
for obj in final_list:
    print(obj.index, obj.score)

#========================== Pronoun replacemnet ===============================

#pr.proReplace(sentences_list,final_list)



print("")    
for obj in final_list:
    summary+=obj.line+"। "


print(bn_tokens.text)
print(" ")
print(summary)


#======================== Evolution ====================================
