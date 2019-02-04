# -*- coding: utf-8 -*-
"""
@author: rksazid
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:13:59 2019

@author: rksazid
"""

import re as regex
from rouge import Rouge

class Sentences:
    def __init__(self, idx, ln, wrds):
        self.index = idx
        self.line = ln
        self.words = wrds
        self.status = True


def avgCalculation(n,m):
    my_summary_file = open('.\Generated Summary\Summary_'+str(n)+'.txt','r', encoding='utf-8')
    my_doc=""
    for s in my_summary_file.readlines():
        my_doc += regex.sub(r'[\n|\\]+','',s)+". "
    #print(my_doc)
    my_summary_file.close()
    
    #print("")
    test_summary_file = open('.\Dataset1\Summaries\Document_'+str(n)+'_Summary_'+str(m)+'.txt','r', encoding='utf-8')
    test_doc=""
    for s in test_summary_file.readlines():
        test_doc += regex.sub(r'[\n|\\]+','',s)+". "
    #print(test_doc)
    #print("")
    test_summary_file.close()
    
    '''
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
    
    
    #======= ROUGE ===========
    hyp = ""
    ref = ""
    for obj in my_sentences_list:
        for w in obj.words:
            hyp+=w+" "
        hyp+=". "
    #print(hyp)
    for obj in test_sentences_list:
        for w in obj.words:
            ref+=w+" "
        ref+=". "
    '''
    rouge = Rouge()
    scores = rouge.get_scores(my_doc, test_doc)
    #print(scores)
    
    
            
    
    
    #print(tp)
    precision = scores[0]['rouge-1']['p']
    #print(precision)
    recall = scores[0]['rouge-1']['r']
    #print(recall)
    fmeasure=scores[0]['rouge-1']['f']
    #print(fmeasure)
    #print(precision,recall,fmeasure)
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
#avgCalculation(2,1)
    
'''
from rouge import Rouge

hypothesis = "বুয়েট রেজিস্ট্রার অধ্যাপক এ কে এম মাসুদ স্বাক্ষরিত ওই বিজ্ঞপ্তির ভাষ্য"

reference = "বুয়েটের রেজিস্ট্রার রেজিস্ট্রার এ কে এম মাসুদ মাসুদ ওই বিজ্ঞপ্তি ভাষ্য"
rouge = Rouge()
scores = rouge.get_scores(hypothesis, reference)
print(scores)
'''

'''
from rouge import FilesRouge

hyp_path = '.\Dataset2\Summaries\Document_2_Summary_1.txt'
ref_path = '.\Generated Summary\Summary_2.txt'

files_rouge = FilesRouge(hyp_path, ref_path)
scores = files_rouge.get_scores(avg=True)
print(scores)

'''

