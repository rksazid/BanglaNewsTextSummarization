# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:16:59 2019

@author: rksazid
"""

import NameRecognition as nr
import CosineSimilarity as csim
import BanglaTokenization as bnTok
import tfidf

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
        self.status = True


    
#================= MAIN ===============================


#-------------- input ------------------
path='.\Dataset1\Documents\Document_1.txt'

input_file = open(path,'r', encoding='utf-8')
doc=input_file.read()
#print(doc)

#------------- tokenization-------------
bn_tokens = bnTok.BengaliTok(doc)
bn_tokens.bn_stop_words()
tokenized_sentences = bn_tokens.bn_sentence_tok(r'[?|।|!]')
#print(tokenized_sentences)
tokenized_words = bn_tokens.bn_word_tok(tokenized_sentences)
#print(tokenized_words)

#------- make a list of Sentence class ----------------
sentences_list = []
ln = len(tokenized_sentences)
for i in range(ln):
    if tokenized_sentences[i]:
        sentences_list.append(Sentences(i,tokenized_sentences[i],tokenized_words[i]))
'''
for obj in sentences_list:
    print(obj.index,obj.line,obj.words)
'''

#   ================= Name recognition  ===================

#print(nr.nameRecognition(sentences_list[19].words))

#=========== TF-IDF Calcualtion For every sentence ============

# ---------- make a list of all token in a document---------
tokenized_documents = []
for lst in tokenized_words:
    tokenized_documents += tokenized_words[lst]

#print(tokenized_documents)

# -------------- tf-idf calculation start-------------
tfidf_obj = tfidf.TFIDF()

i=0
for obj in sentences_list:
    tfidf=0
    for word in obj.words:
        tfidf+=tfidf_obj.tf_idf(word,tokenized_documents,' '.join(tokenized_sentences))
    sentences_list[obj.index].tfidf=tfidf


#=========== Cosine Similarity Calculaion =============

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
   
#print(len(sentences_list[4].line))
for i in range(ln):
    for j in range(ln):
        if i == j:
            continue
        elif sentences_list[i].cos_sim[j] > 0.5:
            if len(sentences_list[i].line) > len(sentences_list[j].line):
                sentences_list[i].sf+=1
                sentences_list[j].status = False
            else:
                sentences_list[j].sf+=1
                sentences_list[i].status = False
                
for obj in sentences_list:
    print(obj.index,obj.line,obj.words,obj.tfidf,obj.cos_sim,obj.status)


'''

for i in range(ln):
    for j in range(ln):
        if i == j:
            continue
        elif sentences_list[i].cos_sim[j] > 0.6:
            if len(sentences_list[i].line) > len(sentences_list[j].line):
                

#----------Stop_words reads-------------------

bn_stw = open('./stop_words.txt','r', encoding='utf-8')
stop_words = "".join(bn_stw.readlines())
stop_words = set(stop_words.split())
#print(stop_words)

#----------regex patterns--------------

pattern_1=r'[,|(|)|-|—|!|"|`|’|‘|“|\?|\\|:|\n]+'
pattern_2=r'[।]+'
pattern_3=r'[\.]'


#----------removing the special charecters-------

doc=regex.sub(pattern_3,':',doc)
#print(doc)
doc=regex.sub(pattern_1,' ',doc)
doc=regex.sub(pattern_2,'.',doc)


sent=sent_tokenize(doc)
#print(sent)

#-------removing the dot (.) character---------

doc=regex.sub(pattern_3,' ',doc)
#print(str)


word = word_tokenize(doc)
#print(word)

#----------- Stop words removing ---------------

word_tokens = [w for w in word if w not in stop_words]
#print(word_tokens)
'''
