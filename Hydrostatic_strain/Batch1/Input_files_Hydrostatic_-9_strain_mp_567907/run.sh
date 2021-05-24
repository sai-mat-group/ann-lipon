#!/bin/bash
module load vasp/6.1.2
mpirun -n 8 vasp_std >& output
