#!/usr/bin/env zsh
#SBATCH -o %J.out
#SBATCH -e %J.err
# source ~/.zshrc
source /hqlf/softwares/module/simu{{version}}.sh
echo 'Run on:' `hostname`
echo 'Start at: ' `date`
echo 'Start MC Simulation at: ' `date`
{{commands}}
echo 'Finish MC Simulation at: ' `date`
echo 'Finish at: ' `date`