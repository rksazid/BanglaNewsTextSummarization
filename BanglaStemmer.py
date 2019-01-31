# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 00:50:57 2019

@author: rksazid
"""

import xml.etree.ElementTree as ET

trees = ET.parse('temp_stemming_xml.xml')
roots = trees.getroot()

def stemming(word_list):
    w=[]
    item=None
    for i in word_list:
        item=None
        for pos in roots.iter(i):
            item=pos.text
        if item is None:
            w.append(i)
        else:
            w.append(item)
    return w