#!/bin/bash

#SBATCH --job-name=ccm3_emanuel_290solar
#SBATCH --output=/scratch/midway/shanshans/ccm3_emanuel_290solar.out
#SBATCH --error=/scratch/midway/shanshans/ccm3_emanuel_290solar.err
#SBATCH --ntasks=1
#SBATCH --partition=sandyb
#SBATCH --time=36:00:00
#SBATCH --mem-per-cpu=32000

module load python
module load netcdf

export PYTHONPATH=$PYTHONPATH:/home/shanshans/CliMT/CliMT-0.6.14/install/lib/python2.7/site-packages

python radiative_convective_equilibrium_ccm3_emanuel_i270_290solar.py
