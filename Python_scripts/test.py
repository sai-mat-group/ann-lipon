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
from pymatgen.transformations.standard_transformations import AutoOxiStateDecorationTransformation, PrimitiveCellTransformation
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
valid_slabs = []
for slab in slabs:
   if not slab.is_polar() and slab.is_symmetric():
       valid_slabs.append(slab)
       
for x in range(len(valid_slabs)):
    #alid_slabs[x].make_supercell([2,1,1])
    sites = valid_slabs[x].get_sorted_structure().sites
    print(len(sites))
    surface_sites = valid_slabs[x].get_surface_sites()
    print(surface_sites)
    sd_list=[]
    layer1_index =[]
    layer1_site = []
    layer2 =[]
    neighbours = []
    for a in range(len(sites)):
                sd_list.append([False,False,False])
    for b in range(len(sites)):
                for c in range(len(surface_sites['top'])):
                    if surface_sites['top'][c][1] not in layer1_index:
                        layer1_index.append(surface_sites['top'][c][1])
                        layer1_site.append(surface_sites['top'][c][0])
                    if sites[b] == surface_sites['top'][c][0]:
                        sd_list[b] = [True,True,True]
                for c in range(len(surface_sites['bottom'])):
                    if surface_sites['bottom'][c][1] not in layer1_index:
                        layer1_index.append(surface_sites['bottom'][c][1])
                        layer1_site.append(surface_sites['bottom'][c][0])
                    if sites[b] == surface_sites['bottom'][c][0]:
                        sd_list[b] = [True,True,True]
    valid_slabs[x].symmetrically_remove_atoms(layer1_index)
    sites = valid_slabs[x].get_sorted_structure().sites
    
    for j in range(len(layer1_site)):
        neighbours = slabs[x].get_neighbors(layer1_site[j],interlayer_spacing)
        for k in range(len(neighbours)):
            if neighbours[k] not in layer2 and neighbours[k] not in layer1_site:
                layer2.append(neighbours[k])
    print(layer2)
    for b in range(len(sites)):
        for c in range(len(layer2)):
            if sites[b] == layer2[c]:
                        sd_list[b] = [True,True,True]
    poscar = Poscar(slabs[x].get_sorted_structure(), selective_dynamics=sd_list)
    os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/test')
    poscar.write_file('%d_POSCAR' %x)

# Any Pymatgen surface method seems to work only for non polar, symmetric slabs. Therefore orignally when I tried to
# remove the first layer and find surface sites again it didnt work because the slab was no longer symmetric or 
# non polar. The current implementation only works for non polar slabs and Im using neighbours to identify the 
# second layer sites using the seperation between the planes as the cutoff radius. POSCAR looks okay for the simpler
# examples.  










