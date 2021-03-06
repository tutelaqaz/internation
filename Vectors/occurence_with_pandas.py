# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 16:13:26 2016

@author: tutela
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist

df = pd.read_csv('test.csv')


selfjoin = pd.merge(df, df, on = 'document_id')
occurrence3=selfjoin.groupby( [ "Ngram_x", "Ngram_y"] ).count().reset_index()
occurrence2 = occurrence3[occurrence3['Ngram_y']!=occurrence3['Ngram_x']]
#for i in nrow(occurrence2):
    #occurrence2[i, ] = sort(occurrence2[i, ])
mask = occurrence2['Ngram_x'] < occurrence2['Ngram_y']
occurrence2['first'] = occurrence2['Ngram_x'].where(mask, occurrence2['Ngram_y'])
occurrence2['second'] = occurrence2['Ngram_y'].where(mask, occurrence2['Ngram_x'])
occurrence2 = occurrence2.drop_duplicates(subset=['document_id', 'first', 'second'])
occurrence2 = occurrence2[['Ngram_x', 'Ngram_y', 'document_id']]
table = (pd.pivot_table(occurrence2, values='document_id', index=['Ngram_x'], 
                        columns = 'Ngram_y', aggfunc=np.sum))
occurrence2.to_csv('test_table2.csv', encoding = 'utf-8', sep = ';')
table = table.fillna(0)
vectors = table.as_matrix()
metric = 'cosine'
distance = pdist(vectors, metric)