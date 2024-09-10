#!/bin/bash

touch set12.cfg
for i in $(ls -d */)
do
	        cd $i 
		bzip2 -d OUTCAR.bz2 
		/home/smart/ann-lipon/mtp/mlp convert-cfg --input-format=vasp-outcar --last OUTCAR temp.cfg
		bzip2 -z OUTCAR
		mv *.cfg ../
		cd ../
		cat temp.cfg >> ./set12.cfg 
		rm temp.cfg
done

