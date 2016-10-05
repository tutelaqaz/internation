# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 13:52:14 2016

@author: tutela
"""

import csv
from time import time
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

words_in_row1 = [] #слова из первой колонки таблицы совстречаемости
words_in_row2 = [] #слова из второй колонки таблицы совстречаемости
occurence = [] #совстречаемость слов из таблицы совстречаемости
vocabular = [] #список всех используемых слов
vectors_list = {} #словарь слов и их совстречаемость
vector = [] #вектор слова
vectors = [] #список всех векторов

start = time()
#функция построения дендограммы
def hierarchy_draw(Z, labels, level):
    fig = plt.figure(figsize=(25, 10))
    hierarchy.dendrogram(Z, labels=labels, color_threshold=level, 
                         leaf_rotation=90, leaf_font_size=10, 
                         count_sort=True,
                         show_contracted=True)
    pp = PdfPages('multipage.pdf')
    fig.savefig(pp, format='pdf')
    pp.close()
    
#чтение и обработка таблицы совстречаемости слов
with open('test_table.csv', 'r', encoding = 'utf-8') as f:
    inputf = csv.reader(f, delimiter = ';')
    for row in inputf:
        words_in_row1.append(row[0])
        words_in_row2.append(row[1])
        occurence.append(row[2])

           
#создание списка всех используемых слов
for word in words_in_row1:
    if word not in vocabular:
        vocabular.append(word)
for word in words_in_row2:
    if word not in vocabular:
        vocabular.append(word)
#сортировка словаря    
vocabular.sort()

#создание словаря слов их совстречаемости по 1 колонке в таблице
for ind, word in enumerate(words_in_row1):
    if word not in vectors_list:   
        vectors_list[word] = {words_in_row2[ind]:occurence[ind]}
    else:
        word_dic = vectors_list[word]
        word_dic[words_in_row2[ind]] = occurence[ind]
        vectors_list[word] = word_dic

#добавление словаря слов их совстречаемости по 2 колонке в таблице       
for ind, word in enumerate(words_in_row2):
    ind = words_in_row2.index(word)
    if word not in vectors_list:   
        vectors_list[word] = {words_in_row1[ind]:occurence[ind]}
    else:
        word_dic = vectors_list[word]
        word_dic[words_in_row1[ind]] = occurence[ind]
        vectors_list[word] = word_dic
words_in_row1 = []        
words_in_row2 = []
occurence = []
#создание списка векторов слов
for word in vocabular:
    word_vector = vectors_list[word]
    for word1 in vocabular:
        if word != word1:
            if word1 in word_vector:
                vector.append(int(word_vector[word1]))
            else:
                vector.append(0)
    vectors.append(vector)
    vector = []
vectors_list = {}
#расчет близости   
distance = pdist(vectors, 'jaccard')
vectors = []
x = 0
line = ''
#Соотнесение близости и слов
#запись близости в таблицу
with open('distance.csv', 'w', encoding='utf-8') as f:
    while x <= len(distance) - 1:
        for ind, word in enumerate(vocabular):
            ind += 1
            while ind <= len(vocabular) - 1:
                string = word +';' + vocabular[ind] + ';' + str(distance[x]) + ';\n'
                f.write(string)
                string = ''
                ind += 1
                x += 1

   
#кластеризация
Z = hierarchy.linkage(distance, method='average' )
#dist.clear()
print('Evaluation time: {}'.format((time()-start)))

#построение дендограммы
hierarchy_draw(Z, vocabular, 0.35)
print('Evaluation time: {}'.format((time()-start)))

print('The end')
            