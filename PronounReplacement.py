# -*- coding: utf-8 -*-
"""
@author: rksazid
"""
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from copy import deepcopy

def proReplace(sent_list,summary):
    readName = open('./HumanName.txt', 'r', encoding='utf-8')
    HumName = " ".join(readName.readlines())
    Name = set(HumName.split())
    #print(Name)
    
    pronouns=["তিনি","তাকে","তাহাকে","সে","ইনি","উনি","তার","তাহার"]
    objective_pronoun=["তাকে","তাহাকে","তার","তাহার"]
    subjective_pronoun=["তিনি","সে","ইনি","উনি"]
    objective_suffix = ["কে","রে","এর"]
    #print(sent_list[0].line)
    for sen in summary:
        for pro in pronouns:
            print(sen.line.find(pro),sen.line)
            print(pro)
    
    

