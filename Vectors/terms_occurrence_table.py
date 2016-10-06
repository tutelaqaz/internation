# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:26:51 2016

@author: tutela
"""
import csv
from time import time

def terms_occurrence_table(start):
    x = 0
    dic = {} # словарь id_doc и всех терминов в нем
    vectors = {} #словарь найденных сочетаний терминов и их количество употреблений
    words_bag = [] # все слова в таблице
    dic_vectors = {} # словарь всех возможных сочетаний терминов


    #Создаем массив со всеми терминами в таблице и словарь, где ключ - id документа,
    # значение - набор терминов встретившихся в документе
    start = time()
    with open('short_test.csv', 'r', encoding = 'utf-8') as f:
        inputf = csv.reader(f, delimiter = ',')
        for row in inputf:
            if x != 0:
                if row[0] not in words_bag:
                    words_bag.append(row[0])
                if row[1] in dic:
                    key = str(row[1])
                    dic[key].append(row[0])
                if row[1] not in dic:
                    key = str(row[1])
                    dic[key] = [row[0]]
            x += 1

    print('Evaluation time: {}'.format((time()-start)))
    
    #сортировка всех слов по алфавиту
    words_bag.sort()
    
    # создание словаря найденных сочетаний терминов и их количество употреблений          
    for key in dic:
        words_in_doc = dic[key]
        for indx, word_in_doc in enumerate(words_in_doc): 
            while indx < len(words_in_doc) - 1:
                indx += 1
                terms = (word_in_doc, words_in_doc[indx])
                if terms in vectors:
                    vectors[terms] += 1
                else:
                    vectors[terms] = 1
    print('Evaluation time: {}'.format((time()-start)))

    #создание словаря словосочетаний и их встречаемости
    for key in vectors:
        combination = [key[0], key[1]]
        combination.sort()
        combination = tuple(combination)
        if combination in dic_vectors:
            value = vectors[key]
            dic_vectors[combination] += value
        else:
            value = vectors[key]
            dic_vectors[combination] = value
        for word2 in words_bag:
            if key[0] != word2:
                combination = [key[0], word2]
                combination.sort()
                combination = tuple(combination)
                if combination not in dic_vectors:
                    dic_vectors[combination] = 0
    print('Evaluation time: {}'.format((time()-start)))   
    
    #запись терминов и их совстречаемости в таблицу
    with open('short_test_table.csv', 'w', encoding = 'utf-8') as f:
        for words in dic_vectors:
            line = words[0] + ';' + words[1] + ';' + str(dic_vectors[words]) + ';\n'
            f.write(line)
        
    print('Evaluation time: {}'.format((time()-start)))         
    
    return words_bag