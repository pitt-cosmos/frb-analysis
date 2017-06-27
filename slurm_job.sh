#!/bin/sh 

#SBATCH -N 1                               # nodes=1 
#SBATCH --ntasks-per-node=1                # ppn=6 
#SBATCH -J FIND_CUTS                       # job name 
#SBATCH -t 90:00:00                        # 90 hours walltime
#SBATCH --mem=4000MB                       # memory in MB 
#SBATCH -p act
#SBATCH --output=logs/1900.out                # file for STDOUT 
#SBATCH --mail-user=yig20@pitt.edu         # Mail  id of the user 
#SBATCH --mail-type=end                    # Slurm will send at the completion of your job 

python find_cuts.py 1900 2000

# end of script 
