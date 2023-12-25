import argparse
from tqdm import tqdm
from collections import Counter

def obtain_vocab_with_thresh(file_path, threshold):
    morphid2freq = Counter()
    with open(file_path) as fp:
        lines = fp.readlines()
        for line in tqdm(lines):
            morph_ids = line.strip().split()
            for morph_id in morph_ids:
                morphid2freq[morph_id] += 1
    vocab = set([morphid_freq[0] for morphid_freq in morphid2freq.most_common() if morphid_freq[1] >= threshold])
    print(f"vocab size: {len(vocab)} words")
    return vocab

def create_morphid2vocabid(vocab):
    morphid2vocabid = {}
    vocabid2morphid = {}
    vocab = sorted(list(vocab))
    for vocabid, morphid in enumerate(vocab):
        morphid2vocabid[morphid] = vocabid
        vocabid2morphid[vocabid] = morphid
    return morphid2vocabid, vocabid2morphid

def make_cooccur_matrix(vocab, file_path, window_size, morphid2vocabid):
    V = len(vocab)
    print(" - initialize cooccur matrix")
    cooccur_matrix = [[0 for _ in range(V)] for _ in tqdm(range(V))]

    print(" - count cooccur")
    with open(file_path) as fp:
        lines = fp.readlines()
        for line in tqdm(lines):
            morphids = line.strip().split()
            for idx, target_morphid in enumerate(morphids):
                if target_morphid not in vocab:
                    continue
                target_vocabid = morphid2vocabid[target_morphid]

                # count co-occurrence of WINDOW_SIZE words before and after
                for w in range(1, window_size + 1):
                    left_idx = idx - w
                    right_idx = idx + w
                    
                    if left_idx >= 0:
                        left_context_morphid = morphids[left_idx]
                        if left_context_morphid in vocab:
                            left_context_vocabid = morphid2vocabid[left_context_morphid]
                            cooccur_matrix[target_vocabid][left_context_vocabid] += 1

                    if right_idx < len(morphids):
                        right_context_morphid = morphids[right_idx]
                        if right_context_morphid in vocab:
                            right_context_vocabid = morphid2vocabid[right_context_morphid]
                            cooccur_matrix[target_vocabid][right_context_vocabid] += 1

    return cooccur_matrix

def write_SVMlight(file_path, cooccur_matrix, vocabid2morphid, threshold):
    output_file_path = file_path[:-4] + f"_threshold-{threshold}_svmlight.txt" 
    with open(output_file_path, "w") as fp:
        for target_vocabid, cooccur_eachrow in enumerate(tqdm(cooccur_matrix)):
            if sum(cooccur_eachrow) == 0:
                continue
            cooccur_nonzero = [f"{vocabid2morphid[vocabid]}:{freq}" for vocabid, freq in enumerate(cooccur_eachrow) if freq > 0]
            target_morphid = vocabid2morphid[target_vocabid]
            fp.write(f"{target_morphid}\t{' '.join(cooccur_nonzero)}\n")
    

def main(args):
    print(args)
    print("obtain_vocab")
    vocab = obtain_vocab_with_thresh(args.file_path, args.threshold)
    print("create_morphid2vocabid")
    morphid2vocabid, vocabid2morphid = create_morphid2vocabid(vocab)
    print("make_cooccur_matrix")
    cooccur_matrix = make_cooccur_matrix(vocab, args.file_path, args.window_size, morphid2vocabid) 
    print("write_SVMlight")
    write_SVMlight(args.file_path, cooccur_matrix, vocabid2morphid, args.threshold)

def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", help="path of magazine_STARTYEAR_ENDYEAR.txt")
    parser.add_argument("-t", "--threshold", type=int, default=1, help="frequency threshold vocab")
    parser.add_argument("-w", "--window_size", type=int, help="count co-occurrence of WINDOWSIZE words before and after")
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli_main()
