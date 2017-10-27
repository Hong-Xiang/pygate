#!/usr/bin/env zsh
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.zshrc
echo 'Run on:' `hostname`
echo 'Start at: ' `date`
{% if merge %}pygate merge{% endif %}
{% if clean %}pygate clean{% endif %}
echo 'Finish at: ' `date`