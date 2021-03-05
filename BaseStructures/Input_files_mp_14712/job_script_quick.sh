# ---------------------------
#PBS -N test_job 
#PBS -q debug
#PBS -l nodes=4
#PBS -l walltime=01:59:00
#PBS -j oe
#PBS -V 
#PBS -m abe 
#PBS -M saigautamg@iisc.ac.in
#PBE -o job.out
#PBE -e error
#---------------------------

#Possible queue options: debug (1-5 nodes, max. 2h), small72 (1-3 nodes; max. 72h), medium (3-5 nodes, max. 48h)
#Below are node specifications
#CPU ONLY : nodes=n:ppn=24:cpu24a
#XEON PHI : nodes=1:ppn=24:xeonphi
#HIGH RAM : nodes=1:ppn=24:hm512g

module load compiler/intel/2018

cd $PBS_O_WORKDIR

VASP_EXEC="/sscu_gpfs/home/gautam/bin/vasp.5.4.4/exec/vasp_std"
mpirun -n 96 ${VASP_EXEC} >& output

