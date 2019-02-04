# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:44:41 2019

@author: rksazid
"""
import re as regex

def BanglanumericDetection(sent_list):
    number_file = open('NumericFigure.txt','r', encoding='utf-8')
    numbers = "".join(number_file.readlines())
    numbers = numbers.split()
    
    
    suffixes = ["টি","টিকে","টির","টা","টাকে","টার","খানা","খানাকে","খানার","খানি","খানিকে","খানির"]
    numpattern=r'[০|১|২|৩|৪|৫|৬|৭|৮|৯]+'
    #w = "হাদিস ১২ কুরআন ১ হাদিস ৫৬৭ হাদিস"
    #print(regex.findall(numpattern,w))
    
    
    s=0
    for obj in sent_list:
        s=0
        s+=len(regex.findall(numpattern,obj.line))
        #print(str(s)+"kkkk")
        for w in obj.words:
            #print(w)
            if w in numbers:
                #print(w)
                s+=1
            for suffix in suffixes:
                lnw = len(w)
                lns = len(suffix)
                if lnw>lns:
                    if w[-lns:] == suffix:
                        if w[:-lns-1] in numbers:
                            s+=1
        obj.nc = s
        #print(obj.words)
        #print(regex.findall(numpattern,obj.line))
        #print(s)
         
#BanglanumericDetection(8)          