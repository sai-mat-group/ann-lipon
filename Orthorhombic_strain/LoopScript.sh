#!/bin/bash

module load vasp/6.1.2
for i in 841 1960 2251 2452 2659 3524 9588 13725 28336 28450 567907 753671 1020019 1235059
do 
	for j in -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 3 4 6 7 9 10
	do	
		cd "orthorhombic_strain_mp_$i"
		cd "Input_files_orthorombic_${j}_strain_mp_${i}"
		mpirun -n 12 vasp_std >& output
		wait
		rm CHG CHGCAR DOSCAR PROCAR vasprun.xml WAVECAR XDATCAR
		bzip2 -z OUTCAR
		cd ../..
	done
done

