#!/bin/bash

#SBATCH --job-name=pc_proxcenb_ssc5L_TL_4p
#SBATCH --error=pc_proxcenb_ssc5L_TL_4p.err
#SBATCH --output=pc_proxcenb_ssc5L_TL_4p.out

#SBATCH --partition=broadwl
#SBATCH --nodes=2
#SBATCH --tasks=44

#SBATCH --account=pi-abbot

#SBATCH --mail-type=ALL
#SBATCH --mail-user=haynes13@uchicago.edu

module load gcc/7.2.0 netcdf-fortran hdf5/1.8.17 openmpi/3.0.0+gcc-7.2.0               

cd /project2/abbot/haynes/ROCKE3D/modelE2_planet_1.0/decks

../exec/runE pc_proxcenb_ssc5L_TL_4p -np 44
