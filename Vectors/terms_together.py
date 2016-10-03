# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:32:39 2016

@author: tutela
"""
import csv
from time import time

x = 0
dic = {} # словарь id_doc и всех терминов в нем
words_bag = [] # все слова в таблице
dic_vectors = {} # словарь всех сочетаний терминов без учета 0

#Создаем массив со всеми терминами в таблице и словарь, где ключ - id документа,
# значение - набор терминов встретившихся в документе
start = time()
with open('ngrams_very_short.csv', 'r', encoding = 'utf-8') as f:
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

#создание словаря словарей, для каждого слова значением будет словарь слов, с
#которыми оно употребляется и в значении - количество словоупотреблений
for key in dic:
    words_in_doc = dic[key]
    for word in words_in_doc:
        if word in dic_vectors:
            word_vectors = dic_vectors[word]
            for word1 in words_in_doc:
                if word1 in word_vectors:
                    word_vectors[word1] += 1
                else:
                    if word != word1:
                        word_vectors[word1] = 1
        else:
            dic_vectors[word] = {}
            for word1 in words_in_doc:
                if word != word1:
                    word_vectors = dic_vectors[word]
                    word_vectors[word1] = 1
#dic.clear()


print('Evaluation time: {}'.format((time()-start)))

#создание таблицы слово - вектор
with open('vectors_numbers2.csv', 'w', encoding = 'utf-8') as f:
    for word in words_bag:
        word_vectors = dic_vectors[word]
        line = word + ';'
        for word1 in words_bag:
            if word != word1:
                if word1 in word_vectors:
                    line += str(word_vectors[word1]) + ','
                else:
                    line += '0,'
        line += ';\n'
        f.write(line)

        
print('Evaluation time: {}'.format((time()-start)))

print('the end')