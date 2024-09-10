# mlip-lipon

This repository contains the density functional theory (DFT) calculated dataset, the trained machine-learned interatomic potentials (MLIP) with the optimal set of hyperparameters, as part of the research manuscript titled **“Investigating Ionic Diffusivity in Amorphous Solid Electrolytes using Machine Learned Interatomic Potentials“** that is available on __.

The goal of the research project is to optimize, construct and evaluate NequIP based MLIPs, on a diverse set of configurations to model and investigate amorphous LiPON. A total of 13,454 configurations were calculated using DFT including Li-rich and Li-poor structures, strained structures and AIMD-based melt-quench structures and slabs, which formed our training (90%) and validation (10%) datasets.

The (**"DFT Dataset"**) folder contains the initial configurations (POSCAR files) and the DFT-calculated, zipped OUTCAR files, and the final configuration (CONTCAR files) for each of the 13,454 configurations. The entire dataset, divided into different subsets has also been included as a 7-zip file (**`Complete_dataset.7z`**) in the extended xyz format, allowing for MLIPs to be trained on different parts of our dataset. The optimized potential has also been provided (**`trained_potential.pth`**) and can be directly used for MD simulations via LAMMPS or other packages.

In case you use any of our data or our trained NequIP potential, we would appreciate a citation to our manuscript at __.
