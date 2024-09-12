# mlip-lipon

This repository contains the density functional theory (DFT) calculated dataset and the trained machine-learned interatomic potentials (MLIP) with the optimal set of hyperparameters, as part of the research manuscript titled **“Investigating Ionic Diffusivity in Amorphous Solid Electrolytes using Machine Learned Interatomic Potentials“** that is under review. A draft of the manuscript is available on [arXiv](http://arxiv.org/abs/2409.06242).

The goal of the research project is to construct, optimize, and evaluate neural equivariant interatomic potential (NequIP) models, on a diverse set of configurations to model and investigate amorphous lithium phosphorous oxynitride (LiPON). A total of 13,454 configurations were calculated using DFT including Li-rich and Li-poor structures, strained structures and *ab initio* molecular dynamics based melt-quench structures and slabs, which formed our training (90%) and validation (10%) datasets.

The (**"DFT Dataset"**) folder contains the initial configurations (POSCAR files) and the DFT-calculated, zipped OUTCAR files, and the final configuration (CONTCAR files) for each of the 13,454 configurations. The entire dataset, divided into different subsets has also been included as a 7-zip file (**`Complete_dataset.7z`**) in the extended xyz format, allowing for MLIPs to be trained on different parts of our dataset. The optimized potential is provided (**`trained_potential.pth`**) and can be directly used for molecular dynamics simulations via [LAMMPS](https://www.lammps.org/) or other packages.

In case you use any of our data or our trained NequIP, we would appreciate a citation to our manuscript at [arxiv](http://arxiv.org/abs/2409.06242).
