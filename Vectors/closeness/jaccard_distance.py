# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 15:14:47 2016

@author: tutela
"""
import csv
import scipy.spatial.distance
from time import time

x = 0
dic_vectors = {} # словарь слово - вектор
vectors_cor = [] #вектор слова
dic_jaccard = {} # словарь близости терминов
start = time()

with open('vectors_numbers2.csv', 'r', encoding='utf-8') as file:
    inputf = csv.reader(file, delimiter = ';')
    for row in inputf:
        word = row[0]
        num1 =''
        for num in row[1]:
            if num != ',':
                num1 += num
            else:
                vectors_cor.append(int(num1))
                num1 = ''
        dic_vectors[word] = vectors_cor
        vectors_cor = []
print('Evaluation time: {}'.format((time()-start)))
        
for word in dic_vectors:
    for word1 in dic_vectors:
        if word != word1:
            vector = dic_vectors[word]
            vector1 = dic_vectors[word1]
            jaccard_closeness = scipy.spatial.distance.jaccard(vector, vector1)
            terms = (word, word1)
            dic_jaccard[terms] = jaccard_closeness
print('Evaluation time: {}'.format((time()-start)))
          
dic_vectors.clear()
dic_vectors_jaccard = {}           
for key in dic_jaccard:
    combination = [key[0], key[1]]
    combination.sort()
    combination = tuple(combination)
    if combination not in dic_vectors_jaccard:
        value = dic_jaccard[key]
        dic_vectors_jaccard[combination] = value
dic_jaccard.clear()
print('Evaluation time: {}'.format((time()-start)))
        
with open('vector_jaccard_distance.csv', 'w', encoding = 'utf-8') as file:
    for key in dic_vectors_jaccard:
        line = key[0] + ', ' + key[1] + ';' + str(dic_vectors_jaccard[key]) + ';\n'
        file.write(line)
print('Evaluation time: {}'.format((time()-start)))
    
print('the end')