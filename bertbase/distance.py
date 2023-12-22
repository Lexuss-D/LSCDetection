import pandas as pd
import numpy as np
from scipy.stats import entropy
from sklearn.metrics.pairwise import cosine_similarity 
from matplotlib import pyplot as plt
from numpy import dot 
from numpy.linalg import norm 

def label_to_distribution(label_list):
    unique_labels, label_counts = np.unique(label_list, return_counts=True)
    total_count = len(label_list)
    probabilities = label_counts / total_count
    return unique_labels, probabilities

def js_divergence(p,q):
    p = np.asarray(p)
    q = np.asarray(q)
    m = (p + q) / 2
    return (entropy(p, m) + entropy(q, m)) / 2

def calculate_js_divergence(list1, list2):
    # Get unique labels and probabilities for each list
    unique_labels1, distribution1 = label_to_distribution(list1)
    unique_labels2, distribution2 = label_to_distribution(list2)

    # Combine unique labels from both lists
    all_labels = np.union1d(unique_labels1, unique_labels2)

    # Create probability distributions with respect to all labels
    prob_dist1 = np.zeros_like(all_labels, dtype=float)
    prob_dist2 = np.zeros_like(all_labels, dtype=float)

    for i, label in enumerate(all_labels):
        if label in unique_labels1:
            prob_dist1[i] = distribution1[unique_labels1 == label]
        if label in unique_labels2:
            prob_dist2[i] = distribution2[unique_labels2 == label]

    # Calculate JS divergence
    js_div = js_divergence(prob_dist1, prob_dist2)
    return js_div

def cosine_distance(p,q):
    return 1.0 - dot(p, q) / (norm(p) * norm(q))

def average_pairwise_distance(old_vectors,new_vectors):
    size_o = len(old_vectors)
    size_n = len(new_vectors)
    sum = 0.0
    for old in old_vectors:
        for new in new_vectors:
            sum += cosine_distance(old,new)
    return sum / size_n /size_o

if __name__=="__main__":

    datapath = "/home/zhidong/github/LSCDetection/bertbase/results"
    wordlist = ['結構','適当','優勝','免許','主張','教授','林檎','写真','椅子',]
    word_jsd = []
    word_apd = []
    for word in wordlist:
        print(f"----------------{word}----------------")
        df = pd.read_csv(f"{datapath}/{word}.tsv",sep='\t')

        print("----------------JSD----------------")
        jsd = calculate_js_divergence(df["old_labels"].to_list(),df["new_labels"].to_list())
        word_jsd.append(jsd)
        print(jsd)

        print("----------------APD----------------")
        apd = average_pairwise_distance([eval(i) for i in df["old_vectors"].to_list()],[eval(i) for i in df["new_vectors"].to_list()])
        word_apd.append(apd)
        print(apd)
    
    out = pd.DataFrame()
    out['word']=wordlist
    out['apd']=word_apd
    out['jsd']=word_jsd
    out.to_csv(f"{datapath}/distance.tsv",sep='\t',index=False)

