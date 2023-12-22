from abc import abstractproperty
from collections import defaultdict
from fcntl import F_UNLCK
import string
import unicodedata
import time
import pandas as pd
import numpy as np
import MeCab
from sklearn import cluster
import torch
import unidic
from tqdm import tqdm
from scipy.stats import entropy
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.metrics import silhouette_score
import logging
from docopt import docopt



'''
Return the best K-Means clustering given the data and the scores of all k values

@para:
    target_word_data : dataframe
    max_range : default [2,10]
@return:
    kmeans : best model of kmeans
    scores : score of each kmeans model
'''
def best_kmeans(input_vectors,max_range=np.arange(2,11)):
    SEED=42
    best_model,best_score=None,-1
    scores=[]
    #print(input_vectors)
    for k in max_range:
        kmeans=KMeans(n_clusters=k,random_state=SEED)
        cluster_labels = kmeans.fit_predict(input_vectors)
        score = silhouette_score(input_vectors, cluster_labels)
        scores.append((k, score))
        if score > best_score:
            best_model, best_score = kmeans, score
        if k==len(input_vectors)-1:#事例数がクラスタ数より少ない場合
          return best_model,scores
    return best_model, scores


'''
recieve the dataframe of target word data, clustering by kmeans
return the dataframe with a column of labels calculated by kmeans

@para : dataframe
@return : dataframe (with new column)
'''
def clustering(target_word_vector_list):
    
    print("clustering vectors amount={}".format(len(target_word_vector_list)))
    kmeans,scores=best_kmeans(target_word_vector_list)
    model=kmeans.fit(target_word_vector_list)

    return model.labels_.tolist()

if __name__=="__main__":
    datapath = "/home/zhidong/github/LSCDetection/bertbase/results"
    wordlist = ["教授","免許","優勝","適当","結構","林檎","写真","椅子","主張",]
    for word in wordlist:
        df = pd.read_csv(f"{datapath}/{word}.tsv",sep='\t')
        print("Clustering")
        old_target_word_vector_list=[eval(i) for i in df["old_vectors"].to_list()]
        new_target_word_vector_list=[eval(i) for i in df["new_vectors"].to_list()]
        labels = clustering(old_target_word_vector_list + new_target_word_vector_list)
        old_labels = labels[:len(labels)//2]
        new_labels = labels[len(labels)//2:]

        df['old_labels'] = old_labels
        df['new_labels'] = new_labels

        df.to_csv(f'/home/zhidong/github/LSCDetection/bertbase/results/{word}.tsv',sep='\t',index=False)
