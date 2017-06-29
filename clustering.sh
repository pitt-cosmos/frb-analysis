#!/bin/sh 

#SBATCH -N 1                               # nodes=1 
#SBATCH --ntasks-per-node=1                # ppn=6 
#SBATCH -J REPROCESS_CUTS                       # job name 
#SBATCH -t 90:00:00                        # 90 hours walltime
#SBATCH --mem=4000MB                       # memory in MB 
#SBATCH --output=logs/cut_800.out                # file for STDOUT 
#SBATCH --mail-user=yig20@pitt.edu         # Mail  id of the user 
#SBATCH --mail-type=end                    # Slurm will send at the completion of your job 

python clustering.py 800 1000

# end of script 
