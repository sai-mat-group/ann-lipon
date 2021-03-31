#!/bin/bash

module load vasp/6.1.2
a=$(pwd)
for i in 1020019 1235059
do
	cd "Input_files_Hydrostatic_-9_strain_mp_$i"
	mpirun -n 8 vasp_std >& output
	wait
	rm CHG CHGCAR DOSCAR PROCAR vasprun.xml WAVECAR XDATCAR
	bzip2 -z OUTCAR
	cd ..
done
