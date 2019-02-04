# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 12:47:47 2019

@author: rksazid
"""

import CheckDocuments as cd
#import Evolution as ev
import ROUGE_score_calculation as rg

w=0.0
for i in range(11):
    for j in range(100):
        #print(j+1)
        cd.generate_summary(j+1,w)
    print(w)
    rg.avgFmeasureCalculation()
    #ev.avgFmeasureCalculation()
    w+=0.1
        