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
from pymatgen.transformations.standard_transformations import AutoOxiStateDecorationTransformation, ConventionalCellTransformation, OxidationStateDecorationTransformation
from pymatgen.transformations.site_transformations import RemoveSitesTransformation
from pymatgen.io.vasp.inputs import Kpoints, Poscar
import math
from pymatgen.io.vasp.sets import MPRelaxSet, MPMetalRelaxSet

# Function to check if coord is between 0 and 1
def frac_check(coord):
    if 0 <= coord <= 1:
        return True
    else:
        return False
    
def layer_check(coord1, coord2):
    if -0.01 <= coord1 - coord2 <= 0.01:
        return True
    else:
        return False

def MP_write_input(slab: Slab, x: float):
    MPobject = MPRelaxSet(structure= slab.get_sorted_structure(), 
                                 user_incar_settings={'NCORE': 6,
                                                      'NSIM': 4,
                                                      'ENCUT': '520 eV',
                                                      'IDIPOL': 3,
                                                      'LCHARG': False,
                                                      'LPLANE': True,
                                                      'EDIFF': 1e-05},
                                 user_kpoints_settings=kpoints,
                                 force_gamma= True)
    miller_index = str(slab.miller_index)
    MPobject.write_input(output_dir = 'polar_surface_index_%s_slab_%d' %(miller_index,x), make_dir_if_not_present=True)
    
    
    
    

#Generates slabs after seperating them as polar and non polar
orig_dir = '/home/smart/Rutvij/'
os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_13725/')
structure = Structure.from_file('POSCAR')
structure = ConventionalCellTransformation().apply_transformation(structure)
structure = AutoOxiStateDecorationTransformation().apply_transformation(structure)
#structure = OxidationStateDecorationTransformation({"Li": 1, "N":-1}).apply_transformation(structure)
list_of_indices = get_symmetrically_distinct_miller_indices(structure, 1)
print(list_of_indices)
all_slabs = []
dipole_moment = []
kpoints = Kpoints.automatic(32)
nonpolar_slabs = []
for index in list_of_indices:
    interlayer_spacing = structure.lattice.d_hkl(index)
    vacuum_layers = math.ceil((20/(interlayer_spacing)))
    slabgen = SlabGenerator(structure, index, 7, vacuum_layers, in_unit_planes=True)
    slabs = slabgen.get_slabs() 
    for x in range(len(slabs)):   
      all_slabs.append(slabs[x])
      if slabs[x].is_polar():
        #os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_13725/polar_slabs/')   
        dipole_moment.append(slabs[x].dipole)
        '''
        MPobject = MPRelaxSet(structure= slabs[x].get_sorted_structure(), 
                                 user_incar_settings={'NCORE': 6,
                                                      'NSIM': 4,
                                                      'ENCUT': '520 eV',
                                                      'IDIPOL': 3,
                                                      'LCHARG': False,
                                                      'LPLANE': True,
                                                      'EDIFF': 1e-05},
                                 user_kpoints_settings=kpoints,
                                 force_gamma= True)
        miller_index = str(index)
        MPobject.write_input(output_dir = 'polar_surface_index_%s_slab_%d' %(miller_index,x), make_dir_if_not_present=True)
        '''
    else:
        #os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_13725/')
        nonpolar_slabs.append(slabs[x])
        '''
        MPobject = MPRelaxSet(structure= slabs[x].get_sorted_structure(), 
                                 user_incar_settings={'NCORE': 6,
                                                      'NSIM': 4,
                                                      'ENCUT': '520 eV',
                                                      'IDIPOL': 3,
                                                      'LCHARG': False,
                                                      'LPLANE': True,
                                                      'EDIFF': 1e-05},
                                 user_kpoints_settings=kpoints,
                                 force_gamma= True)
        miller_index = str(index)
        MPobject.write_input(output_dir = 'nonpolar_surface_index_%s_slab_%d' %(miller_index,x), make_dir_if_not_present=True)
        '''
#for slab in nonpolar_slabs:
surface_sites = nonpolar_slabs[-7].get_surface_sites()
sites = nonpolar_slabs[-7].get_sorted_structure().sites
layer1_index = []
layer1_site = []
sd_list = []
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

print(layer1_site)
layer2 = []
for a in range(len(layer1_site)):
    neighbors = nonpolar_slabs[-10].get_neighbors(layer1_site[c], interlayer_spacing) #Change index
    for b in range(len(neighbors)):
        if neighbors[b] not in layer2 and neighbors[b] not in layer1_site:
          if frac_check(neighbors[b].a) and frac_check(neighbors[b].b) and frac_check(neighbors[b].c):  
            layer2.append(neighbors[b])
interim = []
for b in range(len(sites)):
    for c in range(len(layer2)):
        if layer_check(sites[b].c, layer2[c].c):
            interim.append(sites[b])
for site in interim:
    layer2.append(site)
    
for b in range(len(sites)):
    for c in range(len(layer2)):
        if sites[b] == layer2[c]:
            sd_list[b] = [True,True,True]
            
poscar = Poscar(nonpolar_slabs[-7].get_sorted_structure(), selective_dynamics=sd_list)            
os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_13725/nonpolar_surface_index_(1, 1, 1)_slab_11')
poscar.write_file('POSCAR')

# Any Pymatgen surface method seems to work only for non polar, symmetric slabs. Therefore orignally when I tried to
# remove the first layer and find surface sites again it didnt work because the slab was no longer symmetric or 
# non polar. The current implementation only works for non polar slabs and Im using neighbours to identify the 
# second layer sites using the seperation between the planes as the cutoff radius. POSCAR looks okay for the simpler
# examples.  










