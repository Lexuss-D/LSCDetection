import numpy as np
import pandas as pd
from scipy.stats import spearmanr


def main():
    distance = pd.read_csv('/home/zhidong/github/LSCDetection/bertbase/results/distance.tsv',sep='\t')
    jsd = distance['jsd'].to_list()
    apd = distance['apd'].to_list()
    
    gold = pd.read_csv('/home/zhidong/github/LSCDetection/testsets/jplsc/raw.tsv',sep='\t')
    minus_compare = [-i for i in gold['compare'].to_list()]
    Dlater = gold['Dlater'].to_list()
    absDlater = gold['absDlater'].to_list()

    j_c, p1 = spearmanr(jsd,minus_compare,nan_policy='omit')
    j_d, p2 = spearmanr(jsd,Dlater,nan_policy='omit')
    j_a, p3 = spearmanr(jsd,absDlater,nan_policy='omit')
    a_c, p4 = spearmanr(apd,minus_compare,nan_policy='omit')
    a_d, p5 = spearmanr(apd,Dlater,nan_policy='omit')
    a_a, p6 = spearmanr(apd,absDlater,nan_policy='omit')
    
    eval = pd.DataFrame()
    eval['distance'] = ['jsd','apd']
    eval['compare'] = [j_c,a_c]
    eval['Dlater'] = [j_d,a_d]
    eval['absDlater'] = [j_a,a_a]

    print(eval)
    print(f'{p1},{p2},{p3}\n{p4},{p5},{p6}')
    eval.to_csv('/home/zhidong/github/LSCDetection/bertbase/results/spr.tsv',sep='\t',index=False)

if __name__ == '__main__':
    main()
