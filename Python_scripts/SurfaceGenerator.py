#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 21:07:40 2021

@author: smart
"""

import pymatgen
import numpy as np
import os
from pymatgen.transformations.standard_transformations import ConventionalCellTransformation
from pymatgen.core.surface import SlabGenerator, generate_all_slabs, Slab, get_d
from pymatgen import Lattice, Structure
from pymatgen.io.vasp.inputs import Kpoints, Poscar
import math
from pymatgen.io.vasp.sets import MPRelaxSet, MPMetalRelaxSet


#for generating the slabs
'''
orig_dir = '/home/smart/Rutvij/'
os.chdir(path='/home/smart/Rutvij/BaseStructures/Input_files_mp_1960/')
structure = Structure.from_file('Li2O_mp-1960_conventional_standard.cif')
scrap_list = generate_all_slabs(structure, 1, 20, 10)
list_of_indices = []
list_of_d = []
kpoints = Kpoints.automatic(32)
for x in range(len(scrap_list)):
   if scrap_list[x].miller_index not in list_of_indices:
       list_of_indices.append(scrap_list[x].miller_index)
       list_of_d.append(get_d(scrap_list[x]))
       print(list_of_d)


for y in range(len(list_of_indices)):
   interlayer_spacing = list_of_d[y]
   vacuum_layers = math.ceil((10/(interlayer_spacing*2)))                       
   slabgen = SlabGenerator(structure, list_of_indices[y], 7, vacuum_layers, in_unit_planes=True)
   test_slabs = slabgen.get_slabs()
   os.chdir(path= orig_dir)
   for z in range(len(test_slabs)):    
       MPobject = MPRelaxSet(structure= test_slabs[z] , user_kpoints_settings=kpoints)
       MPobject.write_input(output_dir = 'test_index_%d_slab_%d' %(y,z), make_dir_if_not_present=True)


#for freezing the ionic positions in the bulk of Li2O 110 structure
orig_dir = '/home/smart/Rutvij/'
os.chdir(path='/home/smart/Rutvij/test_index_1_slab_0/')
poscar = Poscar.from_file('POSCAR', check_for_POTCAR=False)
structure = poscar.structure
structure_dict = structure.as_dict()
sd_array = []
values = [0.02273,0.06818,0.11364,0.15909,0.61364,0.56818,0.52273,0.47727]
for x in range(42):
    if round(float(structure_dict['sites'][x]['abc'][2]), 5) in values:
        sd_array.append([True, True, True])
    else:
        sd_array.append([False,False,False])
poscar_write = Poscar(poscar.structure, selective_dynamics=sd_array)
print(poscar_write.selective_dynamics)
poscar_write.write_file('POSCAR')
'''

#Generating surface random structures
list_of_IDs = ['736',
               '841',
               '1960',
               '2452',
               '2659',
               '9588',
               '14712',
               '27687',
               '28336',
               '28450',
               '753671',
               '1020019',
               '1202801',
               '1235059']
orig_dir = '/home/smart/Rutvij/'
kpoints = Kpoints.automatic(32)


#Writing INCAR, KPOINTS, POTCAR and slab structure to POSCAR without SD 
for ID in list_of_IDs:
    os.chdir(path = '/home/smart/Rutvij/BaseStructures/Input_files_mp_%s' %(ID))
    structure_computed = Structure.from_file('POSCAR')
    structure = ConventionalCellTransformation().apply_transformation(structure_computed)
    structure_dict = structure.as_dict()
    scrap_list = generate_all_slabs(structure, 1, 20, 10)
    list_of_indices = []
    list_of_d = []
    list_of_normals = []
    test_slabs = []
    for x in range(len(scrap_list)):
        if scrap_list[x].miller_index not in list_of_indices:
            list_of_indices.append(scrap_list[x].miller_index)
            list_of_d.append(get_d(scrap_list[x]))
            list_of_normals.append(scrap_list[x].normal)

    for y in range(len(list_of_indices)):
       interlayer_spacing = structure.lattice.d_hkl(list_of_indices[y])
       proj_height = (abs(np.dot(np.array([0,0,20]), list_of_normals[y])))
       vacuum_layers = math.ceil((proj_height/(interlayer_spacing)))                       
       slabgen = SlabGenerator(structure, list_of_indices[y], 7, vacuum_layers, in_unit_planes=True)
       test_slabs.append(slabgen.get_slabs())
       for z in range(len(test_slabs[y])):    
           MPobject = MPRelaxSet(structure= test_slabs[y][z], 
                                 user_incar_settings={'NCORE': 6,
                                                      'NSIM': 4,
                                                      'ENCUT': '520 eV',
                                                      'IDIPOL': 3,
                                                      'LCHARG': False,
                                                      'LPLANE': True,
                                                      'EDIFF': 1e-05},
                                 user_kpoints_settings=kpoints,
                                 force_gamma= True)
           MPobject.write_input(output_dir = '%s_surface_index_%d_slab_%d' %(ID,y,z), make_dir_if_not_present=True)
           
'''     
#Overwriting POSCAR with SD                     
           os.chdir(path = '/home/smart/Rutvij/BaseStructures/Input_files_mp_%s' %(ID))
           os.chdir(path = '/home/smart/Rutvij/BaseStructures/Input_files_mp_%s/%s_surface_index_%d_slab_%d' %(ID,ID,y,z))
           sites = test_slabs[z].get_sorted_structure().sites       
           surface_sites = (test_slabs[z].get_surface_sites())
           sd_list = []
           for a in range(len(sites)):
               sd_list.append([False,False,False])
           for x in range(len(sites)):
               for y in range(len(surface_sites['top'])):
                   if sites[x] == surface_sites['top'][y][0]:
                       sd_list[x] = [True,True,True]
               for y in range(len(surface_sites['bottom'])):
                   if sites[x] == surface_sites['bottom'][y][0]:
                       sd_list[x] = [True,True,True]
           poscar_write = Poscar(test_slabs[z].get_sorted_structure(), selective_dynamics=sd_list)
           poscar_write.write_file('POSCAR')        
'''






















