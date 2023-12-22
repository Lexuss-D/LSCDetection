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
from sklearn.decomposition import PCA
from transformers import BertConfig, BertForPreTraining, BertJapaneseTokenizer
import logging
from docopt import docopt

# Path setting
eval_data_path = '/home/zhidong/github/LSCDetection/testsets/jplsc/Graded'
wordlist = ["免許","優勝","適当","結構","林檎","写真","椅子","主張","教授",]
datagroup = ["Earlier","Later","Compare"]

#wordlist = ["主張"]
#datagroup = ["Compare"]


def toVector(target_word,text):
    
    # preprocessing
    table=str.maketrans("!#$%&\'()+,-./:;<=>?@[\\]^_`{|}~「」、。・",' '*len("!#$%&\'()+,-./:;<=>?@[\\]^_`{|}~「」、。・"))
    text = unicodedata.normalize("NFKC", text)
    text=text.translate(table)
    # tokenization
    splited_by_target = text.split("**") # to find the target word index
    #tokens=[]
    tokens_lemma=[]
    length_of_splited=[]
    for part in splited_by_target:
        parsed_text = mecab.parse(part).split('\n')
        tokenized_text_lemma = []
        #tokenized_text = []
        
        for line in parsed_text:
            line=line.strip().split('\t')
            if line[0]!='EOS' and line[0]!='' and len(line[1].split(','))>7: #EOS、空白、记号の解析を除去
                morph_info=line[1].split(',')
                tokenized_text_lemma.append(morph_info[7]) #NWJC-BERTはLemmaで訓練されているので、モデルのVocabに対応するには各トークンをlemmaに置換する必要がある
                #tokenized_text.append(line[0])
        # print("-----------------tokens------------------")
        # print(tokenized_text_lemma)
        tokens_lemma+=tokenized_text_lemma
        length_of_splited.append(len(tokenized_text_lemma))
    #print("-----------------tokens------------------")
    #print(tokens_lemma)
    #print(length_of_splited)

    # transform to token id sequence
    input_tokens = ["[CLS]"] + tokens_lemma[:126] + ["[SEP]"]
    assert len(input_tokens) == sum(length_of_splited)+2

    ids = tokenizer.convert_tokens_to_ids(input_tokens) #add [CLS] and [EOS] into parsed text
    #print("-----------------ids------------------")
    #print(f"{ids[length_of_splited[0]+1]}  {input_tokens[length_of_splited[0]+1]}")
    tokens_tensor = torch.tensor(ids).reshape(1, -1)
    #print("-----------------tokens_tensor------------------")
    #print(tokens_tensor)
    with torch.no_grad():
        output = model(tokens_tensor)
    
    #print(len(output.last_hidden_state)) # size( 1 , sentence length , hidden layer size)
    vector=torch.squeeze(output[0])
    #print("-----------------vector------------------")
    target_word_vector = vector[length_of_splited[0]+1]
    #print(vector)
    
    return target_word_vector.tolist()



if __name__=="__main__":
    # Load Model
    print("Loading Model")
    ckpt = "/home/zhidong/github/LSCDetection/bertbase/nwjc-bert/model.ckpt-2000000"
    config = BertConfig(return_dict=True).from_pretrained("/home/zhidong/github/LSCDetection/bertbase/nwjc-bert/bert_config.json")
    config.vocab_size = 48914
    model = BertForPreTraining(config)
    model.load_tf_weights(config, ckpt)
    model = model.bert
    tokenizer = BertJapaneseTokenizer(vocab_file="/home/zhidong/github/LSCDetection/bertbase/nwjc-bert/vocab.txt", do_lower_case=False)
    mecab = MeCab.Tagger("-r /dev/null -d /home/zhidong/github/LSCDetection/bertbase/unidic-cwj-3.1.0") # in ubuntu, -r \dev\null is nesessary
    print("Model Loaded")


    for word in wordlist:
        old_sentences = []
        new_sentences = []
        print('Usages Deviding')
        for group in datagroup:
            print(f'----------{word}------------')
            df = pd.read_csv(f"{eval_data_path}/{word}/{word}_{group}.tsv",sep="\t")
            if group == 'Earlier':
                print(f'----------{group}------------')
                old_sentences += df['usage1'].to_list()+df['usage2'].to_list()
            elif group == 'Later':
                print(f'----------{group}------------')
                new_sentences += df['usage1'].to_list()+df['usage2'].to_list()
            elif group == 'Compare':
                print(f'----------{group}------------')
                old_sentences += df['usage1'].to_list()
                new_sentences += df['usage2'].to_list()

        assert len(old_sentences)==len(new_sentences)
        
        print("Word representation extracting")
        old_target_word_vector_list = [toVector(word,usage) for usage in tqdm(old_sentences)]
        new_target_word_vector_list = [toVector(word,usage) for usage in tqdm(new_sentences)]

        df = pd.DataFrame()
        df['old_sentences'] = old_sentences
        df['old_vectors'] = old_target_word_vector_list
        df['new_sentences'] = new_sentences
        df['new_vectors'] = new_target_word_vector_list

        df.to_csv(f'/home/zhidong/github/LSCDetection/bertbase/results/{word}.tsv',sep='\t',index=False)
            
            






