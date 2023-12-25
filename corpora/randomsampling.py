import pandas as pd
import random
with open('/home/zhidong/github/LSCDetection/corpora/SHC-magazin/magazine_lemma_1925-2000.txt','r') as f:
    data = f.readlines()

random.seed(114514)
random.shuffle(data)
MAXTOKEN = 5221789
countToken = 0
sampled = []
for line in data:
    sentence = line.strip().split()
    print(len(sentence))
    if countToken <= MAXTOKEN:
        sampled.append(line)
        countToken+=len(sentence)
    else:
        break

with open('/home/zhidong/github/LSCDetection/corpora/SHC-magazin/sampled_magazine_lemma_1925-2000.txt','w') as d:
    d.write(''.join(sampled))

    
    

    
