#!/bin/bash

for i in {22..89}
do
	cd /home/smart/ann-lipon/Defect_structures/Li3PO4_unit_cell/Li_poor/Li5P2N1O6_${i}
	rm EIGENVAL IBZKPT KPOINTS OSZICAR output PCDAT POTCAR REPORT INCAR transformations.json
	cd ../
done

