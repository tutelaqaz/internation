# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 14:54:50 2016

@author: tutela
"""
import csv
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from time import time
from matplotlib.backends.backend_pdf import PdfPages

start = time()
x = 0
vectors = []
words = []

def hierarchy_draw(Z, labels, level):
    fig = plt.figure(figsize=(25, 10))
    hierarchy.dendrogram(Z, labels=labels, color_threshold=level, 
                         leaf_rotation=90, leaf_font_size=3, 
                         count_sort=True)
    pp = PdfPages('multipage.pdf')
    fig.savefig(pp, format='pdf')
    pp.close()

with open('vectors_numbers2.csv', 'r', encoding='utf-8') as file:
    inputf = csv.reader(file, delimiter = ';')
    for row in inputf:
        words.append(row[0])
        vectors_cor = []
        num1 =''
        for num in row[1]:
            if num != ',':
                num1 += num
            else:
                vectors_cor.append(int(num1))
                num1 = ''    
        vectors.append(vectors_cor)
print('Evaluation time: {}'.format((time()-start)))

dist = pdist(vectors, 'cosine')
#vectors.clear()
print('Evaluation time: {}'.format((time()-start)))

Z = hierarchy.linkage( dist, method='average' )
#dist.clear()
print('Evaluation time: {}'.format((time()-start)))


hierarchy_draw(Z, words, 0.35)
print('Evaluation time: {}'.format((time()-start)))

print('the end')