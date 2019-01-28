# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 16:16:59 2019

@author: rksazid
"""

import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize,sent_tokenize
import re as regex
import math
from scipy import linalg, mat, dot
import numpy as np

class BengaliTok:
    def __init__(self, corpus):
        self._bangla_corpus = regex.sub(r'[\n]+','',corpus)
        self.match_obj = regex.search( r'Title:(.*)Text:(.*)', self._bangla_corpus)
        self.title = self.match_obj.group(1)
        self.text = self.match_obj.group(2)
        self.text = regex.sub(r'[\\|;|]','',self.text)
        
        #print(self.title)
        #print(self.text)
        
        #------------- Handling "Qouted" sentence ---------- 
        
        l = len(self.text)
        i=0
        flag=False
        while i < l:
            if (self.text[i]=='"') and (flag==False):
                flag=True
                i=i+1
                continue
            if (self.text[i]=='"') and (flag==True):
                flag=False
                self.text=self.text[:i+1]+"।"+self.text[i+1:]
                #l=l+1
            if flag==True and self.text[i] == '।':
                self.text = self.text[:i]+'#'+self.text[i+1:]
            i=i+1
        #print(self.text)
        
        #--------------------------------------------------

    def bn_stop_words(self):
        #----------Stop_words reads-------------------

        bn_stw = open('./stop_words.txt','r', encoding='utf-8')
        self.stop_words = "".join(bn_stw.readlines())
        self.stop_words = set(self.stop_words.split())
        #print(self.stop_words)
        
        #return stop_words

    def bn_sentence_tok(self, pattern):
        #corpus = self.title + "।" + self.text
        corpus = self.text
        #print(corpus)
        bn_tokens_sen_mod = regex.split(pattern, corpus)
        bn_tokens_sen = [s for s in bn_tokens_sen_mod if s]
        ln=len(bn_tokens_sen)
        for i in range(ln):
            bn_tokens_sen[i] = regex.sub(r'#',"।",bn_tokens_sen[i])

        return bn_tokens_sen

    def bn_word_tok(self,sent_tok):
        word_tokens = {}
        #sent_tok = self.bn_sentence_tok(r'[?|।|!]')
        i=0
        for tokenized_sent in sent_tok:
            tokenized_sent = regex.sub(r'[,|(|)|-|—|!|"|`|’|‘|“|\?|\\|:|\n|।|\.]+','',tokenized_sent)
            word = word_tokenize(tokenized_sent)
            if word:
                word_tokens[i] = [w for w in word if w not in self.stop_words]
            i=i+1
        return word_tokens

class TFIDF():
    def word_frequency(self, word, document):
        #print(document.count(word))
        return document.count(word)

    def word_count(self, document):
        return len(document)

    def word_contain_documents(self, word, documents):
        # number of documents that contain word w
        count = 0
        for doc in documents:
            if (self.word_frequency(word, doc)) > 0:
                count += 1

        return count + 1

    def tf(self, word, document):
        return self.word_frequency(word, document) / self.word_count(document)

    def idf(self, word, documents):
        return math.log(len(documents) / self.word_contain_documents(word, documents))

    def tf_idf(self, word, document, documents):
        return self.tf(word, document) * self.idf(word, documents)



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

def cosSim(w1,w2):
    words_list = set(w1+w2)
    #print(words_list)
    mat1=[]
    mat2=[]
    for w in words_list:
        mat1.append(w1.count(w))
        mat2.append(w2.count(w))
    
    #print(mat1,mat2)
    length = len(mat1)
    m_2d=[[0 for i in range(length)] for j in range(2)]
    
    for i in range(length):
        m_2d[0][i]=mat1[i]
    for i in range(length):
        m_2d[1][i]=mat2[i]
            
    #print(m_2d)
    matrix = mat( m_2d )
    cosim = dot(matrix[0],matrix[1].T)/np.linalg.norm(matrix[0])/np.linalg.norm(matrix[1])
    #print(cosim)
    for n in cosim.A:
        for m in n:
            return m
    
#================= MAIN ===============================


#-------------- input ------------------
path='.\Dataset1\Documents\Document_2.txt'

input_file = open(path,'r', encoding='utf-8')
doc=input_file.read()
#print(doc)

#------------- tokenization-------------
bn_tokens = BengaliTok(doc)
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

#   =================     ===================
print(sentences_list[0].words)
#sentences_list[0].names.append()


#=========== TF-IDF Calcualtion For every sentence ============

# ---------- make a list of all token in a document---------
tokenized_documents = []
for lst in tokenized_words:
    tokenized_documents += tokenized_words[lst]

#print(tokenized_documents)

# -------------- tf-idf calculation start-------------
tfidf_obj = TFIDF()

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
            cosine_sim = cosSim(w1,w2)
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
