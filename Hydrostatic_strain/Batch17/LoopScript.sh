#!/bin/bash

module load vasp/6.1.2
a=$(pwd)
for i in 135 736 841 1960 2251 2452 2659 3524 9588 13725 28336 28450 567907 753671 1020019 1235059
do
	cd "Input_files_Hydrostatic_3_strain_mp_$i"
	mpirun -n 12 vasp_std >& output
	wait
	rm CHG CHGCAR DOSCAR PROCAR vasprun.xml WAVECAR XDATCAR
	bzip2 -z OUTCAR
	cd ..
done
