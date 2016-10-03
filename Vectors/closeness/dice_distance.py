# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 18:21:53 2016

@author: tutela
"""
import csv
import scipy.spatial.distance
import re
from time import time

x = 0
dic_vectors = {} # словарь слово - вектор
vectors_cor = [] #вектор слова
dic_dice = {} # словарь близости терминов
start = time()

# создание словаря термин-ветор
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

#создание словаря термин, термин - близость
for word in dic_vectors:
    for word1 in dic_vectors:
        if word != word1:
            vector = dic_vectors[word]
            vector1 = dic_vectors[word1]
            dice_closeness = scipy.spatial.distance.dice(vector, vector1)
            terms = (word, word1)
            dic_dice[terms] = dice_closeness
print('Evaluation time: {}'.format((time()-start)))

# удаление повторных сочетаний
dic_vectors.clear()               
dic_vectors_dice = {}
for key in dic_dice:
    combination = [key[0], key[1]]
    combination.sort()
    combination = tuple(combination)
    if combination not in dic_vectors_dice:
        value = dic_dice[key]
        dic_vectors_dice[combination] = value
print('Evaluation time: {}'.format((time()-start)))

dic_dice.clear()      
with open('vector_dice_distance.csv', 'w', encoding = 'utf-8') as file:
    for key in dic_vectors_dice:
        line = key[0] + ', ' + key[1] + ';' + str(dic_vectors_dice[key]) + ';\n'
        file.write(line)
print('Evaluation time: {}'.format((time()-start)))
    
print('the end')