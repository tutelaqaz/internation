# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:06:50 2016

@author: tutela
"""
import csv
from time import time
from scipy.spatial.distance import pdist

def terms_distance_table(metric, words_bag, start):
    words_in_row1 = [] #слова из первой колонки таблицы совстречаемости
    words_in_row2 = [] #слова из второй колонки таблицы совстречаемости
    occurence = [] #совстречаемость слов из таблицы совстречаемости
    vectors_list = {} #словарь слов и их совстречаемость
    vector = [] #вектор слова
    vectors = [] #список всех векторов

#чтение и обработка таблицы совстречаемости слов
    with open('short_test_table.csv', 'r', encoding = 'utf-8') as f:
        inputf = csv.reader(f, delimiter = ';')
        for row in inputf:
            words_in_row1.append(row[0])
            words_in_row2.append(row[1])
            occurence.append(row[2])
    
    print('Evaluation time: {}'.format((time()-start)))

#создание словаря слов их совстречаемости по 1 колонке в таблице
    for ind, word in enumerate(words_in_row1):
        if word not in vectors_list:   
            vectors_list[word] = {words_in_row2[ind]:occurence[ind]}
        else:
            word_dic = vectors_list[word]
            word_dic[words_in_row2[ind]] = occurence[ind]
            vectors_list[word] = word_dic
    
    print('Evaluation time: {}'.format((time()-start)))

#добавление словаря слов их совстречаемости по 2 колонке в таблице       
    for ind, word in enumerate(words_in_row2):
        if word not in vectors_list:   
            vectors_list[word] = {words_in_row1[ind]:occurence[ind]}
        else:
            word_dic = vectors_list[word]
            word_dic[words_in_row1[ind]] = occurence[ind]
            vectors_list[word] = word_dic


    print('Evaluation time: {}'.format((time()-start)))
    
#создание списка векторов слов
    for word in words_bag:
        word_vector = vectors_list[word]
        for word1 in words_bag:
            if word != word1:
                if word1 in word_vector:
                    vector.append(int(word_vector[word1]))
                else:
                    vector.append(0)
        vectors.append(vector)
        vector = []

    print('Evaluation time: {}'.format((time()-start)))

#расчет близости   
    distance = pdist(vectors, metric)
    x = 0
#Соотнесение близости и слов
#запись близости в таблицу
    with open('short_distance.csv', 'w', encoding='utf-8') as f:
        while x <= len(distance) - 1:
            for ind, word in enumerate(words_bag):
                ind += 1
                while ind <= len(words_bag) - 1:
                    string = (word +';' + words_bag[ind] + ';' + str(distance[x]) + 
                            ';\n')
                    f.write(string)
                    string = ''
                    ind += 1
                    x += 1
                    
    print('Evaluation time: {}'.format((time()-start)))
    
    return distance
   