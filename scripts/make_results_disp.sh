### THIS SCRIPT PRODUCES RESULTS FOR DISPERSION MEASURES (FD, TD, HD) ON COUNT SPACES ###

declare -a matrixfolder1=$globalmatrixfolder1
declare -a matrixfolder2=$globalmatrixfolder2
declare -a matrixfoldercomb=$globalmatrixfoldercomb
matrixfolders=($globalmatrixfolder1 $globalmatrixfolder2)

# Run model code
corpDir=$corpDir1
outfolder=$countmatrixfolder1
source scripts/run_CNT.sh # Raw Count for first time period
corpDir=$corpDir2
outfolder=$countmatrixfolder2
source scripts/run_CNT.sh # Raw Count for second time period

# Get frequencies
corpDir=$corpDir1
outfolder=$freqresultfolder1
source scripts/run_FREQ.sh # Raw token frequency in first time period
norm=$freqnorm1
source scripts/run_NFREQ.sh # Normalized frequency
corpDir=$corpDir2
outfolder=$freqresultfolder2
source scripts/run_FREQ.sh # Raw token frequency in second time period
norm=$freqnorm2
source scripts/run_NFREQ.sh
infolder=$freqresultfolder1
outfolder=$freqresultfolder1
source scripts/run_TRSF.sh # Log transformation
infolder=$freqresultfolder2
outfolder=$freqresultfolder2
source scripts/run_TRSF.sh
# Subtract values
infolder1=$freqresultfolder1
infolder2=$freqresultfolder2
outfolder=$resultfolder
source scripts/run_DIFF.sh # Subtract frequencies (Frequency Difference)

