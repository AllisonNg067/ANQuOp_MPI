#!/bin/bash -l
#SBATCH --job-name=quop_build
#SBATCH --partition=workq 
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --account=pawsey0309
#SBATCH --output=quop_build.out

module load singularity
singularity remote login --tokenfile=sylabs-token

if [ -e quop_mpi.sif ]
then
	rm quop_mpi.sif

fi


srun -N 1 -n 1 -c 24 singularity build -r quop_mpi.sif quop_mpi.def

