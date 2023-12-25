## Define global parameters ##
parameterfile=scripts/parameters_jp.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
globalmatrixfolderprefix=matrices/fullpara_chj_sampled_jplsc_sim # parent folder for matrices
globalresultfolderprefix=results/fullpara_chj_sampled_jplsc_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh

# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with dispersion measures
globalmatrixfolderprefix=matrices/fullpara_chj_sampled_jplsc_disp # parent folder for matrices
globalresultfolderprefix=results/fullpara_chj_sampled_jplsc_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh

# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores


