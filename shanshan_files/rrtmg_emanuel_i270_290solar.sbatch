#!/bin/bash

#SBATCH --job-name=rrtmg_emanuel_290solar
#SBATCH --output=rrtmg_emanuel_290solar.out
#SBATCH --error=rrtmg_emanuel_290solar.err
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --cpus-per-task=1
#SBATCH --time=36:00:00
#SBATCH --mem-per-cpu=32000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=haynes13@uchicago.edu

module load python/3.5.2

python #SCRIPT#.py
