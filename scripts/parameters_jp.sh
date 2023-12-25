shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
corpDir1="corpora/corpus1/" # directory for corpus1 files (all files in directory will be read)
corpDir2="corpora/corpus2/" # directory for corpus2 files (all files in directory will be read)
#wiCorpDir="corpora/test/corpus_wi/" # directory for word-injected corpus (only needed for Word Injection)
freqnorms=(5222819 5221789) # normalization constants for token frequency (total number of tokens in first and second corpus)
typesnorms=(96447 61666) # normalization constants for number of context types (total number of types in first and second corpus)
windowSizes=(4 5 10 20 30 40) # window sizes for all models
ks=(5) # values for shifting parameter k
ts=(None) # values for subsampling parameter t
iterations=(1) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
dims=(50 100 200 300 350 400) # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
eps=(30) # training epochs for SGNS
targets="testsets/jplsc/targets.tsv" # target words for which change scores should be predicted (one target per line)
testset="testsets/jplsc/targets_input.tsv" # target words in input format (one target per line repeated twice with tab-separation, i.e., 'word\tword', will be created)
#testsetwi="testsets/jplsc/targets_wi.tsv"  # target words in word injection format (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword', will be created)
#goldrankfile="testsets/jplsc/rank_reverse_compare.tsv" # file with gold scores for target words in same order as targets in testsets
goldrankfile="testsets/jplsc/rank_absDlater.tsv" # file with gold scores for target words in same order as targets in testsets
oldclassfile="" # file with gold classes for target words in same order as targets in testsets (leave undefined if non-existent)

# Get normalization constants for dispersion measures
freqnorm1=${freqnorms[0]}
freqnorm2=${freqnorms[1]}
typesnorm1=${typesnorms[0]}
typesnorm2=${typesnorms[1]}

### Make folder structure ###
source scripts/make_folders.sh

### Make target input files ###
source scripts/make_targets.sh