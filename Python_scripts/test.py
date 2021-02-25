#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:20:04 2021

@author: smart
"""

import pymatgen
import numpy as np
import os
from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Slab, get_symmetrically_distinct_miller_indices  
from pymatgen import Lattice, Structure
from pymatgen.transformations.standard_transformations import AutoOxiStateDecorationTransformation
from pymatgen.transformations.site_transformations import RemoveSitesTransformation
from pymatgen.io.vasp.inputs import Kpoints, Poscar
import math
from pymatgen.io.vasp.sets import MPRelaxSet, MPMetalRelaxSet

'''
#Assigns oxidation state to a structure. 
orig_dir = '/home/smart/Rutvij/'
os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/')
structure = Structure.from_file('Li2O_mp-1960_conventional_standard.cif')
structure_charge = AutoOxiStateDecorationTransformation().apply_transformation(structure)
list_of_indices = get_symmetrically_distinct_miller_indices(structure_charge, 1)
interlayer_spacing = structure.lattice.d_hkl(list_of_indices[0])
vacuum_layers = math.ceil((20/(interlayer_spacing)))

#Gets Tasker 3 slabs reconstructed as Tasker 2 Slabs
tasker2_slabs =[]
for y in range(len(list_of_indices)):                       
    slabgen = SlabGenerator(structure_charge, list_of_indices[y], 7, vacuum_layers, in_unit_planes=True)
    slabs = slabgen.get_slabs()
    for z in range(len(slabs)):
        if slabs[z].is_polar():
            print(slabs[z].dipole)
            tasker2_slabs.append(slabs[z].get_tasker2_slabs())
print(tasker2_slabs[1][0].is_polar())
poscar = Poscar(tasker2_slabs[1][0].get_sorted_structure())
os.chdir(orig_dir)
poscar.write_file('POSCAR')        
'''

#Turns on SD for two layers of atoms
orig_dir = '/home/smart/Rutvij/'
os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/')
structure = Structure.from_file('Li2O_mp-1960_conventional_standard.cif')
structure = AutoOxiStateDecorationTransformation().apply_transformation(structure)
list_of_indices = get_symmetrically_distinct_miller_indices(structure, 1)
interlayer_spacing = structure.lattice.d_hkl(list_of_indices[0])
vacuum_layers = math.ceil((20/(interlayer_spacing)))
slabgen = SlabGenerator(structure, list_of_indices[0], 7, vacuum_layers, in_unit_planes=True)
slabs = slabgen.get_slabs()
for x in range(len(slabs)):
    print(slabs[x].is_polar())
    print(slabs[x].is_symmetric())
    slabs[x].make_supercell([2,1,1])
    sites = slabs[x].get_sorted_structure().sites
    print(len(slabs[x].get_sorted_structure().sites))
    surface_sites = slabs[x].get_surface_sites()
    print(surface_sites)
    sd_list=[]
    layer1 =[]
    for a in range(len(sites)):
                sd_list.append([False,False,False])
    for b in range(len(sites)):
                for c in range(len(surface_sites['top'])):
                    if surface_sites['top'][c][1] not in layer1:
                        layer1.append(surface_sites['top'][c][1])
                    if sites[b] == surface_sites['top'][c][0]:
                        sd_list[b] = [True,True,True]
                for c in range(len(surface_sites['bottom'])):
                    if surface_sites['bottom'][c][1] not in layer1:
                        layer1.append(surface_sites['bottom'][c][1])
                    if sites[b] == surface_sites['bottom'][c][0]:
                        sd_list[b] = [True,True,True]
    orignal_slab = slabs[x].copy()
    print(layer1)
    slabs[x] = RemoveSitesTransformation(layer1).apply_transformation(slabs[x])
    print(len(slabs[x].get_sorted_structure().sites))
    surface_sites = slabs[x].get_surface_sites()
    print(surface_sites)
    for b in range(len(sites)):
        for c in range(len(surface_sites['top'])):
            if sites[b] == surface_sites['top'][c][0]:
                        sd_list[b] = [True,True,True]
        for c in range(len(surface_sites['bottom'])):
            if sites[b] == surface_sites['bottom'][c][0]:
                        sd_list[b] = [True,True,True]
    
    poscar = Poscar(orignal_slab.get_sorted_structure(), selective_dynamics=sd_list)
    os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/test')
    poscar.write_file('%d_POSCAR' %x)



# Not working for one of the 111 slabs. Have to check if it is the tasker 3 slab Ans: Surprisingly
# works for the polar slab and not the non-polar one. 
# 










