#!/bin/bash

module load vasp/6.1.2
mpirun -n 12 vasp_std >& output
wait
rm CHG CHGCAR DOSCAR PROCAR vasprun.xml WAVECAR XDATCAR
bzip2 -z OUTCAR

