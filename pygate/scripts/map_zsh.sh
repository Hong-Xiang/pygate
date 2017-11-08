#!/usr/bin/env zsh
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.zshrc
echo 'Run on:' `hostname`
echo 'Start at: ' `date`
if [ ! -d ~/Slurm ]; then
    mkdir ~/Slurm
fi
if [ ! -d {{local_work_directory}} ]; then
    mkdir {{local_work_directory}}
fi
cp {{server_work_directory}}/* {{local_work_directory}}
cd {{local_work_directory}}
{{commands}}
cp {{local_work_directory}}/* {{server_work_directory}}
echo 'Finish at: ' `date`