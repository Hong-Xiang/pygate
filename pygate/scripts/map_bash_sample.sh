#!/bin/bash
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.bashrc
echo 'Run on:' `hostname`
echo 'Start at: ' `date`
if [ ! -d ~/Slurm/tmp/sub.1 ]; then
    mkdir ~/Slurm/tmp/sub.1
fi
cp /tmp/sub.1/* ~/Slurm/tmp/sub.1
cd ~/Slurm/tmp/sub.1

Gate main.mac

cp ~/Slurm/tmp/sub.1/* /tmp/sub.1
echo 'Finish at: ' `date`