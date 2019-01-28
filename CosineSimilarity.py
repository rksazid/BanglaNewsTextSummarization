# -*- coding: utf-8 -*-
"""
@author: rksazid
"""

from scipy import linalg, mat, dot
import numpy as np

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
