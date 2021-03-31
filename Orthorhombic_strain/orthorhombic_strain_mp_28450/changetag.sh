#!/bin/bash

for i in -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 1 3 4 6 7 9 10
do
	cd "Input_files_orthorombic_${i}_strain_mp_28450"
	sed -i 's/Fast/Normal/g' INCAR
	cd ..
done
