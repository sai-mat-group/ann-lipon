#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:46:47 2021

@author: smart
"""

#%% import cell

import pymatgen
import numpy as np
import os
from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Slab, get_symmetrically_distinct_miller_indices  
from pymatgen import Lattice, Structure
from pymatgen.transformations.standard_transformations import AutoOxiStateDecorationTransformation, ConventionalCellTransformation, OxidationStateDecorationTransformation
from pymatgen.transformations.site_transformations import RemoveSitesTransformation
from pymatgen.io.vasp.inputs import Kpoints, Poscar
import math
from pymatgen.io.vasp.sets import MPRelaxSet, MPMetalRelaxSet
from pymatgen.analysis.elasticity.strain import Deformation

# Python3 code to remove whitespace
def remove(string):
	return string.replace(" ", "")
	
#%% 

structure = Structure.from_file('/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/POSCAR')
structure = ConventionalCellTransformation().apply_transformation(structure)
oxi_tranfrom = OxidationStateDecorationTransformation({'Li':1, 'P':5, 'O':-2, 'N':-3})
structure = oxi_tranfrom.apply_transformation(structure)
indices = get_symmetrically_distinct_miller_indices(structure, 2)

loop_list = []
valid_slabs = []
all_slabs =[]
for index in indices:
    interlayer_spacing = structure.lattice.d_hkl(index)
    vacuum_layers = math.ceil((20/(interlayer_spacing)))
    slabgen = SlabGenerator(structure, index, 7, vacuum_layers, in_unit_planes=(True))
    #slab_list = generate_all_slabs(structure, max_index=2, 
    loop_list=slabgen.get_slabs(max_broken_bonds=2)
    for slab in loop_list:
        if not slab.is_polar():
            valid_slabs.append(slab)
        all_slabs.append(slab)
        
print(len(all_slabs), len(valid_slabs))

#%%
kpoints = Kpoints.automatic(32)
for k, slab in enumerate(valid_slabs):
    sd_list=[]
    for a in range(len(slab.sites)):
        sd_list.append([False,False,False])
    surface_sites = slab.get_surface_sites(tag=True)
    surf_index = []
    for i in range(len(surface_sites['top'])):
        loop_index = surface_sites['top'][i][1]
        if loop_index not in surf_index:
            surf_index.append(loop_index)
    for i in range(len(surface_sites['bottom'])):
        loop_index = surface_sites['bottom'][i][1]
        if loop_index not in surf_index:
            surf_index.append(loop_index)
    for a in surf_index:
        sd_list[a] = [True,True,True]
    os.chdir('/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/test/valid_slabs')
    MPobject = MPRelaxSet(structure= slab.get_sorted_structure(), 
                                 user_incar_settings={'NCORE': 16,
                                                      'NSIM': 4,
                                                      'ENCUT': '520 eV',
                                                      'IDIPOL': 3,
                                                      'LCHARG': False,
                                                      'LPLANE': True,
                                                      'EDIFF': 1e-05,
                                                      'EDIFFG':-0.03,
                                                      'ISYM':0,
                                                      'ALGO':'Normal',
                                                      'NSW':150,
                                                      'NELMIN':6},
                                 user_kpoints_settings=kpoints,
                                 force_gamma= True,
                                 user_potcar_functional='PBE_54')
    MPobject.write_input(output_dir = '%s_slab_%d' %(remove(str(slab.formula)),k), make_dir_if_not_present=True)
    os.chdir('%s_slab_%d' %(remove(str(slab.formula)), k))
    poscar = Poscar(slab, comment='%s' %(str(slab.miller_index)), selective_dynamics=sd_list)
    poscar.write_file('POSCAR')     
        
#%% 

        