# -*- coding: utf-8 -*-
"""
@author: rksazid
"""

import re as regex
from nltk.tokenize import word_tokenize


class BengaliTok:
    def __init__(self, corpus,t):
        self._bangla_corpus = regex.sub(r'[\n]+','',corpus)
        if t == "general":
            self.match_obj = regex.search( r'Title:(.*)Text:(.*)', self._bangla_corpus)
            self.title = word_tokenize(self.match_obj.group(1))
            self.text = self.match_obj.group(2)
            self.text = regex.sub(r'[\\|;|]','',self.text)
        else:
            self.text = self._bangla_corpus
        
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
                if i+1 < l:
                    if self.text[i+1]!="।":
                        self.text=self.text[:i+1]+"।"+self.text[i+1:]
            if flag==True and (self.text[i] == '।' or self.text[i] == '?'):
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
        bn_tokens_sen = []
        for s in bn_tokens_sen_mod:
            if s:
                bn_tokens_sen.append(s)
        
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