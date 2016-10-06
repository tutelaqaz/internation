# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 13:52:14 2016

@author: tutela
"""


from time import time
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import terms_occurrence_table as tot
import terms_distance_table as tdt


start = time()
#возможные методы кластеризации
methods = ['single', 'complete', 'average', 'weighted'] 
#возможные метрики расчета близости
metrics = ['cosine', 'jaccard', 'dice', 'cityblock'] 

#функция построения дендограммы
def hierarchy_draw(Z, labels, level):
    fig = plt.figure(figsize=(25, 10))
    hierarchy.dendrogram(Z, labels=labels, color_threshold=level, 
                         leaf_rotation=90, leaf_font_size=5, 
                         count_sort=True,
                         show_contracted=True)
    pp = PdfPages('short_dendogramm.pdf')
    fig.savefig(pp, format='pdf')
    pp.close()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--distance", required = True, 
                    help = ("Choose distance metric: 'cosine', 'jaccard', " +
                    "'dice', 'cityblock'"), 
                    action = "store", 
                    type = str)
parser.add_argument("-m", "--method", required = True, 
                    help = ("Choose clustering method: 'single', 'complete', " +
                    "'average', 'weighted'"),
                    action = "store", type = str)
                    
args = vars(parser.parse_args())

cl_method = args['method']
metric = args['distance']
'''
metric = 'cityblock'
cl_method = 'weighted'
'''
if cl_method not in methods:
    print('Error: You chould choose one of the following methods: \n' +
          "'single', 'complete', 'average', 'weighted'")
elif metric not in metrics:
    print('Error: You chould choose one of the following methods: \n' +
          "'cosine', 'jaccard', 'dice', 'cityblock'")
else:
#создание таблицы совстречаемости и списка всех слов  
    words_bag = tot.terms_occurrence_table(start) 

#создание таблицы близости и матрицы близости  
    distance = tdt.terms_distance_table(metric, words_bag, start)

#кластеризация
    Z = hierarchy.linkage(distance, method=cl_method )

    print('Evaluation time: {}'.format((time()-start)))

#построение дендограммы
    hierarchy_draw(Z, words_bag, 0.35)

    print('Evaluation time: {}'.format((time()-start)))

    print('The end')          