#!/bin/bash

for i in 135 736 841 1960 2251 2452 2659 3524 9588 13725 28336 28450 567907 753671 1020019 1235059
do 	
		
		cd "Input_files_Hydrostatic_-9_strain_mp_$i"
		rm EIGENVAL IBZKPT INCAR KPOINTS OSZICAR output PCDAT POTCAR REPORT
		cd ../
done


