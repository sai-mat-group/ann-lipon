#!/bin/bash
# ---------------------------
#PBS -N Hydrostatic_Strain
#PBS -q batch
#PBS -l nodes=43:ncpus=24
#PBS -l walltime=00:59:00
#PBS -j oe
#PBS -V
#PBE -o job.out
#PBE -e error
#---------------------------

#Possible queue options
#idqueue: 24-256 cores; 1h wall-time
#small: 24-1032; 24hr; 3 running jobs/user + 2 queued
#small72: 24-1032; 72hr; 1 job/user + 1 queued
#medium: 1033-8208; 24hr; 1 job/user + 1 queued
#large: 8209-24000; 24hr; Authorized users only; 1 job/user + 1 queued
#batch: default queue that all jobs are placed. Route the jobs to queue depending on parameters.

#Below are node specifications
#CPU ONLY : nodes=n:ncpus=24

module unload PrgEnv-cray PrgEnv-gnu PrgEnv-intel
module load PrgEnv-intel/6.0.5
module unload gcc intel
module load intel/19.0.5.281
module unload craype-haswell craype-sandybridge craype-ivybridge
module load craype-haswell
module unload craype
module load craype/2.6.1
module unload cray-mpich
module load cray-mpich/7.7.10
module unload cray-libsci
module load cray-libsci/19.06.1
module unload fftw
module load cray-fftw/3.3.8.3
export CRAYPE_LINK_TYPE=dynamic

cd $PBS_O_WORKDIR

VASP_EXEC="/home/proj/ug/17/ugsagar/bin/vasp.6.1.2/vasp_std"

#Change -n according to the number of nodes chosen, should be no_of_nodes*24
#-N should be 24 always

file='n4.txt'
cwd="$(pwd)"
#nod=24

while IFS="," read -r name nod
#for name in `seq 11 13`
do

	cd "$name"
	aprun -n $nod -N 24 ${VASP_EXEC} > output & 
	cd "$cwd"
#done	
done < $file
wait
