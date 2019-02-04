# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:13:59 2019

@author: rksazid
"""

import re as regex
import BanglaTokenization
import BanglaStemmer as bs
import CosineSimilarity as csim

class Sentences:
    def __init__(self, idx, ln, wrds):
        self.index = idx
        self.line = ln
        self.words = wrds
        self.cos_sim = []
        self.status = True


def avgCalculation(n,m):
    my_summary_file = open('.\Generated Summary\Summary_'+str(n)+'.txt','r', encoding='utf-8')
    my_doc=""
    for s in my_summary_file.readlines():
        my_doc += regex.sub(r'[\n|\\]+','',s)+"। "
    #print(my_doc)
    my_summary_file.close()
    
    #print("")
    test_summary_file = open('.\Dataset1\Summaries\Document_'+str(n)+'_Summary_'+str(m)+'.txt','r', encoding='utf-8')
    test_doc=""
    for s in test_summary_file.readlines():
        test_doc += regex.sub(r'[\n|\\]+','',s)+"। "
    #print(test_doc)
    #print("")
    test_summary_file.close()
    
    my_tokenizer = BanglaTokenization.BengaliTok(my_doc,"test")
    my_tokenizer.bn_stop_words()
    my_tokenized_sentences = my_tokenizer.bn_sentence_tok(r'[?|।|!]')
    my_tokenized_words = my_tokenizer.bn_word_tok(my_tokenized_sentences)
    #make a list of Sentence class
    my_sentences_list = []
    ln1 = len(my_tokenized_words)    
    
    for i in range(ln1):
        if my_tokenized_sentences[i]:
            my_sentences_list.append(Sentences(i,my_tokenized_sentences[i],
                                            my_tokenized_words[i]))
    
    #====== Stemming ========
    for obj in my_sentences_list:
        obj.words=bs.stemming(obj.words)
    
    test_tokenizer = BanglaTokenization.BengaliTok(test_doc,"test")
    test_tokenizer.bn_stop_words()
    test_tokenized_sentences = test_tokenizer.bn_sentence_tok(r'[?|।|!]')
    test_tokenized_words = test_tokenizer.bn_word_tok(test_tokenized_sentences)
    #make a list of Sentence class
    test_sentences_list = []
    ln2 = len(test_tokenized_words)    
    
    for i in range(ln2):
        if test_tokenized_sentences[i]:
            test_sentences_list.append(Sentences(i,test_tokenized_sentences[i],
                                            test_tokenized_words[i]))
    
    #====== Stemming ========
    for obj in test_sentences_list:
        obj.words=bs.stemming(obj.words)
        
    #====== tokens print ========
#    for obj in my_sentences_list:
#        print(obj.words)
        
#    print(" ")
#    for obj in test_sentences_list:
#        print(obj.words)
        
    # ========== Cosim ===========
    for i in range(ln1):
        for j in range(ln2):
            w1=my_sentences_list[i].words
            w2=test_sentences_list[j].words
            cosine_sim = csim.cosSim(w1,w2)
            my_sentences_list[i].cos_sim.append(cosine_sim)
    
    #for obj in my_sentences_list:
    #    print(obj.line,obj.words,obj.cos_sim)
    tp=0
    for obj in my_sentences_list:
        for v in obj.cos_sim:
            if v > 0.9:
                tp+=1
    #print(tp)
    precision = tp/ln1
    #print(precision)
    recall = tp/ln2
    #print(recall)
    if precision==0 and recall==0:
        return 0,0,0
    fmeasure=(2*precision*recall)/(precision+recall)
    #print(fmeasure)
    #print(n,m,precision,recall,fmeasure)
    return precision,recall,fmeasure

def fmeasure(n):
    avg_precision=0.0
    avg_recall=0.0
    avg_fmeasure=0.0
    for i in range(1,4):
        precision,recall,fmeasure = avgCalculation(n,i)
        avg_precision+=precision
        avg_recall+=recall
        avg_fmeasure+=fmeasure
        
    avg_precision/=3
    avg_recall/=3
    avg_fmeasure/=3
    #print(avg_precision,avg_recall,avg_fmeasure)
    #print(n)
    return avg_precision,avg_recall,avg_fmeasure



def avgFmeasureCalculation():
    all_avg_precision=0.0
    all_avg_recall=0.0
    all_avg_fmeasure=0.0
    
    for i in range(1,101):
        #print(i)
        p,r,f = fmeasure(i)
        #print("")
        all_avg_precision+=p
        all_avg_recall+=r
        all_avg_fmeasure+=f
        
    all_avg_precision/=100
    all_avg_recall/=100
    all_avg_fmeasure/=100
    print(all_avg_precision,all_avg_recall,all_avg_fmeasure)
    
avgFmeasureCalculation()