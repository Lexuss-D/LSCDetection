import pandas as pd
import sys

def main(args):
    with open(args,'r',encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            line = line.strip().split('\t')
            line[1] = line[1].replace('.','-').split('/')[1].split('-')
            line[1] = '\t'.join(line[1])
            line = '\t'.join(line)
            print(line)
    




if __name__ == '__main__':
    # args = sys.argv
    args = '/hdd/repository/LSCDetection/results/extent_shc_sampled_extent_disp/spr_reverse_compare.tsv'
    main(args)

